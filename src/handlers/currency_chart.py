from aiogram import Router
# from aiogram.types import Message, CallbackQuery, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.filters import Command
# from aiogram.utils import InlineKeyboardBuilder, InlineKeyboardButton

# from ..service.charts_defs import get_currency_rates, create_chart

currency_chart_router = Router()

# def get_currency_keyboard():
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="Гривня", callback_data="currency:UAH")],
#         [InlineKeyboardButton(text="Польська злота", callback_data="currency:PLN")],
#         [InlineKeyboardButton(text="Американський долар", callback_data="currency:USD")],
#         [InlineKeyboardButton(text="Євро", callback_data="currency:EUR")]
#     ])
#     return keyboard

# @currency_chart_router.message(Command("currencyChart"))
# async def show_balance(message: Message):
#     await message.answer("Виберіть валюту:", reply_markup=get_currency_keyboard())

# @currency_chart_router.callback_query(lambda c: c.data and c.data.startswith("currency:"))
# async def handle_currency_choice(callback_query: CallbackQuery):
#     currency = callback_query.data.split(":")[1]
#     rates = get_currency_rates(currency)
#     chart_buf = create_chart(rates, currency)
#     photo = BufferedInputFile(chart_buf.read(), filename="chat.png")
#     await message.answer_photo(photo=photo)
