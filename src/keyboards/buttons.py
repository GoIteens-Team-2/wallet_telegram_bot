from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Router

buttons_router = Router()

def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="USD")],
            [KeyboardButton(text="EUR")],
            [KeyboardButton(text="GBP")]
        ],
        resize_keyboard=True
    )
