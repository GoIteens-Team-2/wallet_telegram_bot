from aiogram import Router
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, Message

from ..service.currency import get_currency_rates, create_chart

currency_chart_router = Router()


@currency_chart_router.message(Command("currencyChart"))
async def ask_currency_type(message: Message):
    await message.answer("Введіть базову валюту для створення графіка (USD, UAH, PLN, EUR):")

@currency_chart_router.message()
async def get_currency_chart(message: Message):
    currencys_type = message.text
    rates = get_currency_rates()
    chart_buf = create_chart(rates, currency_type=currencys_type)
    photo = BufferedInputFile(chart_buf.read(), filename="chart.png")
    await message.answer_photo(photo=photo)