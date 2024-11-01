# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# def transaction_history_keyboard():
#     """Створює клавіатуру з командами для перегляду історії."""
#     return ReplyKeyboardMarkup(
#         keyboard=[
#             [KeyboardButton(text="/historyExpenses - Історія останньої витрати")],
#             [KeyboardButton(text="/historyIncomes - Історія ваших доходів")],
#             [
#                 KeyboardButton(text="/historyFromDate - Історія витрат конкретного числа")
#             ],
#             [
#                 KeyboardButton(text="Головне меню", request_contact=True)
#             ]
#         ],
#         resize_keyboard=True,
#         one_time_keyboard=True
#     )

# async def send_keyboard_example(message):
#     kb = ReplyKeyboardMarkup(
#         keyboard=[[KeyboardButton(text="Надати контакт", request_contact=True)]],
#         resize_keyboard=True,
#         one_time_keyboard=True
#     )
#     await message.answer("Будь ласка, надайте свій контакт:", reply_markup=kb)
