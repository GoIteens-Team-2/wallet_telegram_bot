import os
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import json
from datetime import datetime
from aiogram.fsm.context import FSMContext


from ..service.MessageState import MessageState
from ..service.data_management import data_manager
from ..service.monthlyTransactions import (
    load_user_transactions,
    generate_monthly_transaction_graph,
    group_transactions_by_month,
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
            transaction["date"] = datetime.now().strftime("%m-%d")

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
            transaction["date"] = datetime.strftime("%m-%d")

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
        "Введіть дату у форматі DD-MM, з якої ви хочете побачити транзакції:"
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
            filter_date = datetime.strptime(input_date, "%d-%m")
        except ValueError:
            await message.answer(
                "Неправильний формат дати. Будь ласка, введіть у форматі DD-MM."
            )
            user_input_dates[user_id] = None
            return

        transactions = user_data.get(str(user_id), {}).get("transactions", [])

        filtered_transactions = [
            t
            for t in transactions
            if datetime.strptime(t["date"], "%d-%m") >= filter_date
        ]

        if not filtered_transactions:
            await message.answer("Немає транзакцій з цієї дати.")
            user_input_dates[user_id] = None
            return

        transactions_history = "\n".join(
            [
                f"{idx+1}. {t['description']} на {t['amount']} грн (Дата: {t['date']})"
                for idx, t in enumerate(filtered_transactions)
            ]
        )

        await message.answer(f"Транзакції з {input_date}:\n{transactions_history}")

        user_input_dates[user_id] = None



@history_router.message(Command("monthlyTransactionsGraph"))
async def send_transaction_history(message: Message):
    user_id = message.from_user.id
    transactions = load_user_transactions(user_id)

    if not transactions:
        await message.answer("У вас немає транзакцій за цей місяць")
        return

    monthly_income, monthly_expenses = group_transactions_by_month(transactions)

    graph = generate_monthly_transaction_graph(monthly_income, monthly_expenses)
    await message.answer_photo(graph, caption="Графік транзакцій помісячно")

