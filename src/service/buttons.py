from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Прибуток"), KeyboardButton("Витрати"))
    keyboard.add(KeyboardButton("Мій баланс"), KeyboardButton("Що таке wallet-bot?"))
    return keyboard

def transaction_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Історія транзакцій"))
    return keyboard
