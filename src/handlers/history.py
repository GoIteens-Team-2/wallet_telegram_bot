import json
from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext


from ..states.MessageState import MessageState

from ..service.data_management import data_manager
from ..service.history import (
    load_user_transactions,
    filter_transactions_by_date,
    group_transactions,
    generate_transaction_buffer,
)

from ..enums.DateType import DateType
from ..keyboards import get_inline_keyboard

history_router = Router()


user_data = {}

user_input_dates = {}


@history_router.message(Command("testhistory"))
async def show_transaction_history_options(message: Message):
    buttons = {
        "Історія витрат": "history_expenses",
        "Історія доходів": "history_incomes",
        "Історія конкретноі дати": "history_from_date",
    }
    await message.answer(
        "°ОБЕРІТЬ КОМАНДИ ДЛЯ ПЕРЕГЛЯДУ°",
        reply_markup=get_inline_keyboard(
            btns=buttons,
            sizes=(1,) * len(buttons),
        ),
    )


@history_router.message(Command("historyExpenses"))
@history_router.callback_query(F.data == "history_expenses")
async def transaction_history_expenses(event: Message | CallbackQuery):
    user_id = event.from_user.id
    if isinstance(event, CallbackQuery):
        event = event.message

    data_manager.load_user_data(user_id)

    transactions = data_manager.user_data[user_id].get("transactions", [])
    for transaction in transactions:
        if "date" not in transaction:
            transaction["date"] = datetime.now().strftime("%d-%m-%y")

    data_manager.save_user_data(user_id)
    with open(f"{user_id}_transactions.json", "w", encoding="utf-8") as json_file:
        json.dump(data_manager.user_data[user_id], json_file, indent=4)
    expenses = [t for t in transactions if t["type"] == "expense"]
    if not expenses:
        await event.answer("У вас немає витрат.")
        return

    history_expenses = "\n".join(
        [
            f"{idx+1}. {t['description']} на {t['amount']} грн (Дата: {t['date']})"
            for idx, t in enumerate(expenses)
        ]
    )
    await event.answer(f"Історія ваших витрат:\n{history_expenses}")


@history_router.message(Command("historyIncomes"))
@history_router.callback_query(F.data == "history_incomes")
async def transaction_history_incomes(event: Message | CallbackQuery):
    user_id = event.from_user.id
    if isinstance(event, CallbackQuery):
        event = event.message

    data_manager.load_user_data(user_id)
    transactions = data_manager.user_data[user_id].get("transactions", [])

    for transaction in transactions:
        if "date" not in transaction:
            transaction["date"] = datetime.strftime("%d-%m-%y")

    data_manager.save_user_data(user_id)
    with open(f"{user_id}_transactions.json", "w", encoding="utf-8") as json_file:
        json.dump(data_manager.user_data[user_id], json_file, indent=4)

    incomes = [t for t in transactions if t["type"] == "income"]
    if not incomes:
        await event.answer("У вас немає витрат.")
        return

    history_incomes = "\n".join(
        [
            f"{idx+1}. {t['amount']} за {t['description']} грн (Дата: {t['date']})"
            for idx, t in enumerate(incomes)
        ]
    )

    await event.answer(f"Історія ваших доходів:\n{history_incomes}")


@history_router.message(Command("historyFromDate"))
@history_router.callback_query(F.data == "history_from_date")
async def ask_for_date(event: Message | CallbackQuery, state: FSMContext):
    if isinstance(event, CallbackQuery):
        event = event.message
    await state.set_state(MessageState.quest_1)
    await event.answer(
        "Введіть дату у форматі DD-MM-YY, з якої ви хочете побачити транзакції:"
    )


@history_router.message(MessageState.quest_1)
async def transaction_from_date(message: Message, state: FSMContext):
    await state.clear()

    user_id = message.from_user.id
    user_input_dates[user_id] = None

    if user_id in user_input_dates and user_input_dates[user_id] is None:
        input_date = message.text
        user_input_dates[user_id] = input_date

        try:
            filter_date = datetime.strptime(input_date, "%d-%m-%y")
        except ValueError:
            await message.answer(
                "Неправильний формат дати. Будь ласка, введіть у форматі DD-MM-YY",
                reply_markup=get_inline_keyboard(
                    btns={"Скасувати введення": "cancel_form"}, sizes=(1,)
                ),
            )
            user_input_dates[user_id] = None
            return

        transactions = user_data.get(str(user_id), {}).get("transactions", [])

        filtered_transactions = [
            t
            for t in transactions
            if datetime.strptime(t["date"], "%d-%m-%y") >= filter_date
        ]

        if not filtered_transactions:
            await message.answer("Немає транзакцій з цієї дати.")
            user_input_dates[user_id] = None
            return

        transactions_history = "\n".join(
            [
                f"{idx+1}. {t['description']} на {t['amount']} грн)"
                for idx, t in enumerate(filtered_transactions)
            ]
        )

        await message.answer(f"Транзакції з {input_date}:\n{transactions_history}")

        user_input_dates[user_id] = None


@history_router.message(Command("historyFromTo"))
@history_router.callback_query(F.data == "history_from_to")
async def ask_first_date(event: Message | CallbackQuery, state: FSMContext):
    if isinstance(event, CallbackQuery):
        event = event.message
    await state.set_state(MessageState.quest_3)

    await message.answer("Введіть першу дату у форматі dd-mm-yyyy:")


@history_router.message(MessageState.quest_3)
async def handle_first_date(message: Message, state: FSMContext):
    await state.update_data(quest_4=message.text)
    await state.set_state(MessageState.quest_4)

    first_date_text = message.text.strip()
    try:
        first_date = datetime.strptime(first_date_text, "%d-%m-%y").date()
        await state.update_data(first_date=first_date)
        await message.answer("Тепер введіть другу дату у форматі dd-mm-yy:")
    except ValueError:
        await message.answer(
            "Невірний формат дати. Правильний дати: dd-mm-yy.\nАбо натисніть на кнопка для скасування введення.",
            reply_markup=get_inline_keyboard(
                btns={"Скасувати введення": "cancel_form"}, sizes=(1,)
            ),
        )


@history_router.message(MessageState.quest_4)
async def handle_second_date(message: Message, state: FSMContext):
    await state.clear()

    second_date_text = message.text.strip()
    user_id = message.from_user.id
    try:
        second_date = datetime.strptime(second_date_text, "%d-%m-%y").date()
        user_data = await state.get_data()
        first_date = user_data.get("first_date")
        if first_date and first_date > second_date:
            await message.answer("Перша дата не має бути більше другої")
            return
        transactions = load_user_transactions(user_id)
        if not transactions:
            await message.answer("У вас немає транзакцій")
            return
        filtered_transactions = filter_transactions_by_date(
            transactions, first_date, second_date
        )
        if filtered_transactions:
            result = "Транзакції між {} й {}:\n".format(
                first_date.strftime("%d-%m-%y"), second_date.strftime("%d-%m-%y")
            )
            for transaction in filtered_transactions:
                result += f"- {transaction['date']}: {transaction['type']} {transaction['amount']} грн., {transaction['description']}\n"
            await message.answer(result)
        else:
            await message.answer("Транзакцій в цьому діапазоні немає")
    except ValueError:
        await message.answer(
            "Невірний формат дати. Правильний дати: dd-mm-yy",
            reply_markup=get_inline_keyboard(
                btns={"Скасувати введення": "cancel_form"}, sizes=(1,)
            ),
        )


@history_router.message(Command("historyPlot"))
@history_router.callback_query(F.data == "history_plot")
async def send_transaction_history(event: Message | CallbackQuery ):
    user_id = message.from_user.id
    if isinstance(event, CallbackQuery):
        event = event.message
    transactions = load_user_transactions(user_id)

    if not transactions:
        await message.answer("У вас немає транзакцій")
        return
    try:
        monthly_income, monthly_expenses = group_transactions(
            transactions["transactions"], DateType.MONTHLY
        )

        graph = generate_transaction_buffer(
            monthly_income, monthly_expenses, DateType.MONTHLY
        )
    except TypeError:
        await message.answer("Неправильний формат дати для генерації графіку.")
        return

    graph_image = BufferedInputFile(graph.read(), "plot.png")
    await message.answer_photo(photo=graph_image, caption="Графік транзакцій помісячно")


@history_router.message(Command("historyPlotDay"))
@history_router.callback_query(F.data == "history_plot_day")
async def send_transaction_history(message: Message):
    user_id = message.from_user.id
    if isinstance(event, CallbackQuery):
        event = event.message
    transactions = load_user_transactions(user_id)

    if not transactions:
        await message.answer("У вас немає транзакцій")
        return

    try:
        daily_income, daily_expenses = group_transactions(
            transactions["transactions"], DateType.DAILY
        )

        graph = generate_transaction_buffer(
            daily_income, daily_expenses, DateType.DAILY
        )
    except TypeError:
        await message.answer("Неправильний формат дати для генерації графіку.")
        return

    graph_image = BufferedInputFile(graph.read(), "plot.png")
    await message.answer_photo(
        photo=graph_image, caption="Графік ваших транзакцій(поденно)"
    )


@history_router.callback_query(F.data == "cancel_form")
async def cancel_entering(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.answer("Введення скасовано")
