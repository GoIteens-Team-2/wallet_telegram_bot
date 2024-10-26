from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from src.service.data_management import data_manager
from ..keyboards.buttons import main_menu_keyboard


info_router = Router()


@info_router.message(CommandStart())
async def commandstart(message: Message):
    user_id = message.from_user.id
    data_manager.load_user_data(user_id)
    welcome_message = (
        "Привіт! Я wallet-bot, чи просто бот гаманець. У мої функції уходить транзакції та конвертація валют, "
        "з описом того на шо була транзакція (за вашим бажанням). "
        "Однією з особливостей цього бота, буде конвертація валют у криптовалюту, Єфір, Біткоїн тощо. "
        "Але ця функція ще розроб`ляється :'("
        "Якщо потрібна допомога впишіть команду '/help'"
    )
    await message.answer(welcome_message, reply_markup=main_menu_keyboard())


@info_router.message(F.text == "/balance")
async def show_balance(message: Message):
    user_id = message.from_user.id
    data_manager.load_user_data(user_id)
    await message.answer(
        f"Ваш поточний баланс: {data_manager.user_data[user_id]['balance']} грн."
    )


@info_router.message(F.text == "/help")
async def show_balance(message: Message):
    user_id = message.from_user.id
    data_manager.load_user_data(user_id)
    help_message = (
        f"Ось доступні команди:\n"
        f"/income {{сума}} {{опис}} - Додати дохід\n"
        f"/expense {{сума}} {{опис}} - Додати витрату\n"
        f"/history - Переглянути історію транзакцій\n"
        f"/balance - переглянути свій баланс"
    )
    await message.answer(help_message)
