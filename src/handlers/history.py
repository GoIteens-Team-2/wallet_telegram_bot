import os
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import json
from datetime import datetime
from aiogram.fsm.context import FSMContext


from ..service.MessageState import MessageState
from ..service.data_management import data_manager
from ..service.history_defs import (
    load_user_transactions,
    generate_monthly_transaction_graph,
    group_transactions_by_month,
    filter_transactions_by_date,
    group_transactions_by_day,
    generate_daily_transaction_graph
)

history_router = Router()


user_data = {}

user_input_dates = {}


@history_router.message(Command("historyExpenses"))
async def transaction_history(message: Message):
    user_id = message.from_user.id
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
        await message.answer("У вас немає витрат.")
        return

    history_expenses = "\n".join(
        [
            f"{idx+1}. {t['description']} на {t['amount']} грн (Дата: {t['date']})"
            for idx, t in enumerate(expenses)
        ]
    )

    await message.answer(f"Історія ваших витрат:\n{history_expenses}")


@history_router.message(Command("historyIncomes"))
async def transaction_history(message: Message):
    user_id = message.from_user.id
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
        await message.answer("У вас немає витрат.")
        return

    history_incomes = "\n".join(
        [
            f"{idx+1}. {t['amount']} за {t['description']} грн (Дата: {t['date']})"
            for idx, t in enumerate(incomes)
        ]
    )

    await message.answer(f"Історія ваших доходів:\n{history_incomes}")


@history_router.message(Command("historyFromDate"))
async def ask_for_date(message: Message, state: FSMContext):
    await state.set_state(MessageState.quest_1)
    await message.answer(
        "Введіть дату у форматі DD-MM-YY, з якої ви хочете побачити транзакції:"
    )


@history_router.message(MessageState.quest_1)
async def transaction_from_date(message: Message, state: FSMContext):
    await state.update_data(quest_2=message.text)
    await state.set_state(MessageState.quest_2)


    user_id = message.from_user.id
    user_input_dates[user_id] = None


    if user_id in user_input_dates and user_input_dates[user_id] is None:
        input_date = message.text
        user_input_dates[user_id] = input_date

        try:
            filter_date = datetime.strptime(input_date, "%d-%m-%y")
        except ValueError:
            await message.answer(
                "Неправильний формат дати. Будь ласка, введіть у форматі DD-MM-YY"
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
async def ask_first_date(message: Message, state: FSMContext):
    await state.update_data(quest_3=message.text)
    await state.set_state(MessageState.quest_3)

    await message.answer("Введіть першу дату у форматі dd-mm-yy:")

@history_router.message(MessageState.quest_3)
async def handle_first_date(message: Message, state: FSMContext):
    await state.update_data(quest_4=message.text)
    await state.set_state(MessageState.quest_4)

    first_date_text = message.text.strip()
    try:
        first_date = datetime.strptime(first_date_text, '%d-%m-%y').date()
        await state.update_data(first_date=first_date)
        await message.answer("Тепер введіть другу дату у форматі dd-mm-yy:")
    except ValueError:
        await message.answer("Невірний формат дати. Правильний дати: dd-mm-yy")


@history_router.message(MessageState.quest_4)
async def handle_second_date(message: Message, state: FSMContext):
    second_date_text = message.text.strip()
    user_id = message.from_user.id
    try:
        second_date = datetime.strptime(second_date_text, '%d-%m-%y').date()
        user_data = await state.get_data()
        first_date = user_data.get('first_date')
        if first_date and first_date > second_date:
            await message.answer("Перша дата не має бути більше другої")
            return
        transactions = load_user_transactions(user_id)
        if not transactions:
            await message.answer("У вас немає транзакцій")
            return
        filtered_transactions = filter_transactions_by_date(transactions, first_date, second_date)
        if filtered_transactions:
            result = "Транзакції між {} й {}:\n".format(first_date.strftime('%d-%m'), second_date.strftime('%d-%m'))
            for transaction in filtered_transactions:
                result += f"- {transaction['date']}: {transaction['type']} {transaction['amount']} грн., {transaction['description']}\n"
            await message.answer(result)
        else:
            await message.answer("Транзакцій в цьому діапазоні немає")
    except ValueError:
        await message.answer("Невірний формат дати. Правильний дати: dd-mm-yy")





@history_router.message(Command("historyPlot"))
async def send_transaction_history(message: Message):
    user_id = message.from_user.id
    transactions = load_user_transactions(user_id)

    if not transactions:
        await message.answer("У вас немає транзакцій")
        return

    monthly_income, monthly_expenses = group_transactions_by_month(transactions)

    graph = generate_monthly_transaction_graph(monthly_income, monthly_expenses)
    await message.answer_photo(graph, caption="Графік транзакцій помісячно")




@history_router.message(Command("historyPlotDay"))
async def send_transaction_history(message: Message):
    user_id = message.from_user.id
    transactions = load_user_transactions(user_id)
    
    if not transactions:
        await message.answer("У вас немає транзакцій")
        return
    
    daily_income, daily_expenses = group_transactions_by_day(transactions)
    
    graph = generate_daily_transaction_graph(daily_income, daily_expenses)
    await message.answer_photo(graph, caption="Графік ваших транзакцій(поденно)")