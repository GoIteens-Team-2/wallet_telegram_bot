from aiogram import Router, F
from aiogram.types import Message
from ..service.currency import get_currency_rates, create_chart

currency_chart_router = Router()


@currency_chart_router.message(F.text == "/currencyChart")
async def show_balance(message, update):
    def currency(update):
        rates = get_currency_rates()
        chart_buf = create_chart(rates)
        update.message.reply_photo(photo=chart_buf)

    await message.answer(currency())
