from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from ..service.data_management import data_manager

history_router = Router()

@history_router.message(Command("history"))
@history_router.message(F.text == "Історія")
async def transaction_history(message: Message):
    user_id = message.from_user.id
    data_manager.load_user_data(user_id)
    transactions = data_manager.user_data[user_id].get("transactions", [])
    if not transactions:
        await message.answer("У вас немає транзакцій.")
        return
    history = "\n".join([f"{idx+1}. {t['type'].capitalize()}: {t['description']} на {t['amount']} грн" for idx, t in enumerate(transactions)])
    await message.answer(f"Історія ваших транзакцій:\n{history}")
