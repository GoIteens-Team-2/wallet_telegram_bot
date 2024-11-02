from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def transaction_history_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/historyExpenses")],
            [KeyboardButton(text="/historyIncomes")],
            [KeyboardButton(text="/historyFromDate")],
            [KeyboardButton(text="Головне меню")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

async def send_keyboard_example(message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Надати контакт", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Будь ласка, надайте свій контакт:", reply_markup=kb)
