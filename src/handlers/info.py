from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardButton
from src.service.data_management import data_manager


info_router = Router()


@info_router.message(CommandStart(deep_link=True))
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
        f"Ось доступні команди:\n"
        f"/income {{сума}} {{опис}} - Додати дохід\n"
        f"/expense {{сума}} {{опис}} - Додати витрату\n"
        f"/historyIncomes - переглянути ВСЮ історію доходів\n"
        f"/historyExpenses - переглянути ВСЮ історію витрат\n"
        f"/historyFromDate - переглянути історію транзакцій які були виконані у певну дату\n"
        f"/balance - переглянути свій баланс"
        f"/history - поглиблина історія транзакцій"
    )
    await message.answer(help_message)


@info_router.message(Command("history"))
async def command_history(message: Message):
    user_id = message.from_user.id
    data_manager.load_user_data(user_id)
    history_message = "Команди ваших Транзакцій:"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Історія доходів", callback_data="historyIncomes")],
        [InlineKeyboardButton(text="Історія витрат", callback_data="historyExpenses")],
        [InlineKeyboardButton(text="Історія за датою", callback_data="historyFromDate")],
        [InlineKeyboardButton(text="Баланс", callback_data="balance")]
    ])
    
    await message.answer(history_message, reply_markup=keyboard)
