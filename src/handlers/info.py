from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from ..service.data_management import data_manager

info_router = Router()

@info_router.message(CommandStart())
async def commandstart(message: Message):
    user_id = message.from_user.id
    data_manager.load_user_data(user_id) 
    welcome_message = (
        f"Вітаємо, якщо потрібна допомога по боту впишіть команду '/help'"
    )
    await message.answer(welcome_message)

@info_router.message(F.text == "Прибуток")
async def request_income_info(message: Message):
    await message.answer("Будь ласка, введіть дохід у форматі: /income {сума} {опис}")

@info_router.message(F.text == "Витрати")
async def request_expense_info(message: Message):
    await message.answer("Будь ласка, введіть витрату у форматі: /expense {сума} {опис}")


@info_router.message(F.text == "мій баланс")
async def show_balance(message: Message):
    user_id = message.from_user.id
    data_manager.load_user_data(user_id)
    await message.answer(f"Ваш поточний баланс: {data_manager.user_data[user_id]['balance']} грн.")

@info_router.message(F.text == "/help")
async def show_balance(message: Message):
    user_id = message.from_user.id
    data_manager.load_user_data(user_id)
    help_message = (
        f"Ваш поточний баланс: {data_manager.user_data[user_id]['balance']} грн.\n"
        f"Ось доступні команди:\n"
        f"/income {{сума}} {{опис}} - Додати дохід\n"
        f"/expense {{сума}} {{опис}} - Додати витрату\n"
        f"/history - Переглянути історію транзакцій"
    )
    await message.answer(help_message)    
@info_router.message(Command="about")
async def about_command(message: Message):
    about_message = (
        "Привіт! Я wallet-bot, чи просто бот гаманець. У мої функції уходить транзакції та конвертація валют, "
        "з описом того на шо була транзакція (за вашим бажанням). "
        "Однією з особливостей цього бота, буде конвертація валют у криптовалюту, Єфір, Біткоїн тощо. "
        "Але ця функція ще розробляється :'("
    )
    await message.answer(about_message)
