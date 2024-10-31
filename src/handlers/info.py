from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
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

 def get_history_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="Історія доходів", callback_data="history:incomes"),
        InlineKeyboardButton(text="Історія витрат", callback_data="history:expenses"),
    )
    keyboard.row(
        InlineKeyboardButton(text="Транзакції від дати", callback_data="history:from_date"),
        InlineKeyboardButton(text="Баланс", callback_data="history:balance"),
    )
    return keyboard.as_markup()

@info_router.message(Command("history"))
async def command_history(message: Message):
    await message.answer("Історії транзакцій:", reply_markup=get_history_keyboard())

# Обробники callback_data для історії транзакцій
@info_router.callback_query(lambda c: c.data == "history:incomes")
async def history_incomes(callback_query: CallbackQuery):
    await callback_query.message.answer("Команда: /historyIncomes")
    await callback_query.answer()

@info_router.callback_query(lambda c: c.data == "history:expenses")
async def history_expenses(callback_query: CallbackQuery):
    await callback_query.message.answer("Команда: /historyExpenses")
    await callback_query.answer()

@info_router.callback_query(lambda c: c.data == "history:from_date")
async def history_from_date(callback_query: CallbackQuery):
    await callback_query.message.answer("Команда: /historyFromDate")
    await callback_query.answer()

@info_router.callback_query(lambda c: c.data == "history:balance")
async def history_balance(callback_query: CallbackQuery):
    await callback_query.message.answer("Команда: /balance")
    await callback_query.answer(
