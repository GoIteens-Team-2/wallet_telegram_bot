from aiogram import Router
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command

from ..service.charts_defs import get_currency_rates, create_chart

currency_chart_router = Router()


@currency_chart_router.message(Command("currencyChart"))
async def show_balance(message: Message):
    currency = "UAH"  # FROM COMMAND
    rates = get_currency_rates(currency)
    chart_buf = create_chart(rates, currency)
    photo = BufferedInputFile(chart_buf.read(), filename="chat.png")
    await message.answer_photo(photo=photo)
