from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from ..service.data_management import data_manager


info_router = Router()


@info_router.message(CommandStart(deep_link=True))
async def command_start(message: Message):
    welcome_message = (
        "Привіт! Я wallet-bot, чи просто бот гаманець. У мої функції входять транзакції та конвертація валют "
        "з описом того, на що була транзакція (за вашим бажанням). "
        "Однією з особливостей цього бота буде конвертація валют у криптовалюту — Ефір, Біткоїн тощо. "
        "Але ця функція ще розробляється :(\n\n"
        "Якщо потрібна допомога, впишіть команду '/help'."
    )
    await message.answer(welcome_message)


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
    "📋 *Доступні команди:*\n\n"
    "➕ /income {сума} {опис} - Додати дохід\n"
    "➖ /expense {сума} {опис} - Додати витрату\n\n"
    "📈 /historyIncomes - Переглянути всю історію доходів\n"
    "📉 /historyExpenses - Переглянути всю історію витрат\n\n"
    "📅 /historyFromTo - Введіть дві дати, щоб отримати всі транзакції за цей період\n"
    "📊 /historyPlot - Графік надходжень та витрат (помісячно)\n"
    "📆 /historyPlotDay - Графік надходжень та витрат (поденно)\n\n"
    "🗓️ /historyFromDate - Переглянути транзакції за певну дату\n"
    "💰 /balance - Переглянути поточний баланс\n"
    )
    await message.answer(help_message)
