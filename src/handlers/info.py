from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardButton
from src.service.data_management import data_manager
from keyboards import transaction_history_keyboard


info_router = Router()

@info_router.message(CommandStart(deep_link=True))
async def command_start(message: Message):
    user_id = message.from_user.id
    data_manager.load_user_data(user_id)
    welcome_message = (
        "Привіт! Я wallet-bot, чи просто бот гаманець. У мої функції входять транзакції та конвертація валют "
        "з описом того, на що була транзакція (за вашим бажанням). "
        "Однією з особливостей цього бота буде конвертація валют у криптовалюту — Ефір, Біткоїн тощо. "
        "Але ця функція ще розробляється :(\n\n"
        "Якщо потрібна допомога, впишіть команду '/help'."
    )
    await message.answer(welcome_message)
    await message.answer(
        "Вітаємо! Ось доступні опції:",
        reply_markup=transaction_history_keyboard()
    )



@info_router.message(Command("balance"))
async def show_balance(message: Message):
    user_id = message.from_user.id
    data_manager.load_user_data(user_id)
    await message.answer(
        f"Ваш поточний баланс: {data_manager.user_data[user_id]['balance']} грн."
    )


@info_router.message(Command("help"))
async def show_help(message: Message):
    user_id = message.from_user.id
    data_manager.load_user_data(user_id)
    help_message = (
        f"Ось доступні команди:\n"
        f"/income {{сума}} {{опис}} - Додати дохід\n"
        f"/expense {{сума}} {{опис}} - Додати витрату\n"
        f"/historyIncomes - переглянути ВСЮ історію доходів\n"
        f"/historyExpenses - переглянути ВСЮ історію витрат\n"
        f"/historyFromTo - користувач пише дві дати і бот видає всі транзакції які були виконані в цьому періоді\n"
        f"/historyPlot - графік надходжень/витрат помісячно\n"
        f"/historyPlotDay - графік надходжень/витрат поденно\n"
        f"/historyFromDate - переглянути історію транзакцій які були виконані у певну дату\n"
        f"/balance - переглянути свій баланс\n"
        f"/history - поглиблина історія транзакцій\n"
    )
    await message.answer(help_message)
