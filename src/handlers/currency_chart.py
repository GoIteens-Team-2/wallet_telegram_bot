from aiogram import Router
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command

from ..service.charts_defs import get_currency_rates, create_chart

currency_chart_router = Router()

@currency_chart_router.message(Command("currencyChart"))
async def show_balance(message: Message):
    rates = get_currency_rates()
    chart_buf = create_chart(rates)
    photo = BufferedInputFile(chart_buf.read(), filename="chat.png")
    await message.answer(photo=photo)