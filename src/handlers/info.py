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
"📌 *Команди для управління фінансами:*\n\n"
    "💰 *Дохід та витрати*\n"
    "   ➕ /income {сума} {опис} — Додати дохід\n"
    "   ➖ /expense {сума} {опис} — Додати витрату\n\n"
    
    "📊 *Історія транзакцій*\n"
    "   🔹 /history_incomes — Переглянути всю історію доходів\n"
    "   🔸 /history_expenses — Переглянути всю історію витрат\n"
    "   📆 /history_from_to — Введіть дві дати для перегляду транзакцій \n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tза цей період\n"
    "   📅 /history_from_date — Переглянути транзакції за обрану дату\n\n"
    "   📈 /history_plot_monthly — Графік доходів/витрат (помісячно)\n"
    "   📉 /history_plot_day — Графік доходів/витрат (поденно)\n"
    
    "💼 *Інше*\n"
    "   🏦 /balance — Переглянути поточний баланс\n"
    
    "💱 *Обмін валют*\n"
    "   🔄 /exchange {сума} {валюта} — Перевести суму з однієї валюти в іншу\n"
    "   📉 /currency_chart — Показати графік курсів валют\n" 
    )
    await message.answer(help_message)
