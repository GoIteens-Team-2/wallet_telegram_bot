from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import BufferedInputFile

from ..service.currency import get_currency_rates, create_chart

currency_chart_router = Router()


@currency_chart_router.message(Command("currencyChart"))
async def get_currency_chart(message: Message):
    rates = get_currency_rates()
    chart_buf = create_chart(rates)
    photo = BufferedInputFile(chart_buf.read(), filename="chart.png")
    await message.answer_photo(photo=photo)
