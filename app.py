import json
import asyncio
from config import token
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token=token)
dp = Dispatcher(storage=MemoryStorage())

user_data = {}

def load_user_data(user_id):
    file_name = f"user_{user_id}_data.json"
    try:
        with open(file_name, 'r', encoding="utf-8") as file:
            user_data[user_id] = json.load(file)
    except FileNotFoundError:
        user_data[user_id] = {"balance": 0, "transactions": []}

def save_user_data(user_id):
    file_name = f"user_{user_id}_data.json"
    with open(file_name, 'w', encoding="utf-8") as file:
        json.dump(user_data[user_id], file, indent=4)

keyboared = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Старт")],
        [KeyboardButton(text="Прибуток")],
        [KeyboardButton(text="Ваш баланс")],
        [KeyboardButton(text="Витрати")],
        [KeyboardButton(text="Історія")]
    ],
    resize_keyboard=True
)


async def commandstart(message: Message):
    user_id = message.from_user.id
    load_user_data(user_id)
    welcome_message = (
        f"Вітаємо, {message.from_user.first_name}!\n"
        f"Ваш поточний баланс: {user_data[user_id]['balance']} грн.\n"
        f"Ось доступні команди:\n"
        f"/income {{сума}} {{опис}} - Додати дохід\n"
        f"/expense {{сума}} {{опис}} - Додати витрату\n"
        f"/history - Переглянути історію транзакцій"
    )
    await message.answer(welcome_message)

async def request_income_info(message: Message):
    await message.answer("Будь ласка, введіть дохід у форматі: /income {сума} {опис}")

async def show_balance(message: Message):
    user_id = message.from_user.id
    load_user_data(user_id)
    await message.answer(f"Ваш поточний баланс: {user_data[user_id]['balance']} грн.")

async def request_expense_info(message: Message):
    await message.answer("Будь ласка, введіть витрату у форматі: /expense {сума} {опис}")

async def show_history(message: Message):
    user_id = message.from_user.id
    load_user_data(user_id)
    transactions = user_data[user_id].get("transactions", [])
    if not transactions:
        await message.answer("У вас немає транзакцій.")
        return
    history = "\n".join([f"{idx+1}. {t['type'].capitalize()}: {t['description']} на {t['amount']} грн" for idx, t in enumerate(transactions)])
    await message.answer(f"Історія ваших транзакцій:\n{history}")

async def add_income(message: Message):
    user_id = message.from_user.id
    load_user_data(user_id)
    try:
        command_parts = message.text.split(maxsplit=2)
        amount = float(command_parts[1])
        description = command_parts[2] if len(command_parts) > 2 else "Доход"
    except (IndexError, ValueError):
        await message.answer("Будь ласка, введіть правильну команду у форматі: /income {сума} {опис}")
        return
    user_data[user_id]["balance"] += amount
    user_data[user_id]["transactions"].append({"type": "income", "amount": amount, "description": description})
    save_user_data(user_id)
    await message.answer(f"Доход '{description}' на суму {amount} грн додано. Ваш новий баланс: {user_data[user_id]['balance']} грн.")

async def add_expense(message: Message):
    user_id = message.from_user.id
    load_user_data(user_id)
    try:
        command_parts = message.text.split(maxsplit=2)
        amount = float(command_parts[1])
        description = command_parts[2] if len(command_parts) > 2 else "Витрата"
    except (IndexError, ValueError):
        await message.answer("Будь ласка, введіть правильну команду у форматі: /expense {сума} {опис}")
        return
    if user_data[user_id]["balance"] < amount:
        await message.answer(f"Недостатньо коштів на балансі для цієї витрати. Ваш поточний баланс: {user_data[user_id]['balance']} грн.")
        return
    user_data[user_id]["balance"] -= amount
    user_data[user_id]["transactions"].append({"type": "expense", "amount": amount, "description": description})
    save_user_data(user_id)
    await message.answer(f"Витрату '{description}' на суму {amount} грн додано. Ваш новий баланс: {user_data[user_id]['balance']} грн.")

async def transaction_history(message: Message):
    user_id = message.from_user.id
    load_user_data(user_id)
    transactions = user_data[user_id].get("transactions", [])
    if not transactions:
        await message.answer("У вас немає транзакцій.")
        return
    history = "\n".join([f"{idx+1}. {t['type'].capitalize()}: {t['description']} на {t['amount']} грн" for idx, t in enumerate(transactions)])
    await message.answer(f"Історія ваших транзакцій:\n{history}")

dp.message.register(commandstart, CommandStart())
dp.message.register(request_income_info, lambda message: message.text == "Прибуток")
dp.message.register(show_balance, lambda message: message.text == "Ваш баланс")
dp.message.register(request_expense_info, Command("Витрати"))
dp.message.register(show_history, lambda message: message.text == "Історія")
dp.message.register(add_income, Command("income"))
dp.message.register(add_expense, Command("expense"))
dp.message.register(transaction_history, Command("history"))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
