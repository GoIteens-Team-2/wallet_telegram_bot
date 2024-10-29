from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Router

buttons_router = Router()

def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="USD")],
            [KeyboardButton(text="EUR")],
            [KeyboardButton(text="GBP")], 
            [KeyboardButton(text="Історії транзакцій")],
            KeyboardButton(text="Графік валют")], 
        ],
        resize_keyboard=True
    )

def transaction_history_keyboard():
    """Створює клавіатуру з командами для перегляду історії."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/historyExpenses - Історія останньої витрати")],
            [KeyboardButton(text="/historyIncomes - Історія ваших доходів")],
            [KeyboardButton(text="/historyFromDate - Історія витрат конкретного числа")],
            [KeyboardButton(text="Головне меню")]  # Кнопка для повернення до головного меню
        ],
        resize_keyboard=True
    )
