from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import datetime

from ..service.data_management import data_manager
from ..buttons import transaction_history_keyboard


transaction_router = Router()

@transaction_router.message(Command("income"))
async def add_income(message: Message):
    user_id = message.from_user.id
    data_manager.load_user_data(user_id)
    try:
        command_parts = message.text.split(maxsplit=2)
        amount = float(command_parts[1])
        description = command_parts[2] if len(command_parts) > 2 else "Доход"
        data = message.date.strftime('%d-%m-%y')
    except (IndexError, ValueError):
        await message.answer("Будь ласка, введіть правильну команду у форматі: /income {сума} {опис}")
        return
    data_manager.user_data[user_id]["balance"] += amount
    data_manager.user_data[user_id]["transactions"].append({"type": "income", "amount": amount, "description": description, "date": data})
    data_manager.save_user_data(user_id)
    await message.answer(f"Доход '{description}' на суму {amount} грн додано. Ваш новий баланс: {data_manager.user_data[user_id]['balance']} грн.")

@transaction_router.message(Command("expense"))
async def add_expense(message: Message):
    user_id = message.from_user.id
    data_manager.load_user_data(user_id)
    try:
        command_parts = message.text.split(maxsplit=2)
        amount = float(command_parts[1])
        description = command_parts[2] if len(command_parts) > 2 else "Витрата"
        data = message.date.strftime('%d-%m-%y')
    except (IndexError, ValueError):
        await message.answer("Будь ласка, введіть правильну команду у форматі: /expense {сума} {опис}")
        return
    if data_manager.user_data[user_id]["balance"] < amount:
        await message.answer(f"Недостатньо коштів на балансі для цієї витрати. Ваш поточний баланс: {data_manager.user_data[user_id]['balance']} грн.")
        return
    data_manager.user_data[user_id]["balance"] -= amount
    data_manager.user_data[user_id]["transactions"].append({"type": "expense", "amount": amount, "description": description, "date": data})
    data_manager.save_user_data(user_id)
    await message.answer(f"Витрату '{description}' на суму {amount} грн додано. Ваш новий баланс: {data_manager.user_data[user_id]['balance']} грн.")
