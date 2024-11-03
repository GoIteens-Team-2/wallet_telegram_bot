from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, Message, CallbackQuery

from ..service.currency import get_currency_rates, create_chart
from ..keyboards import get_inline_keyboard
from ..constants import SELECTED_CURRENCIES

currency_chart_router = Router()


@currency_chart_router.message(Command("currency_chart"))
async def ask_currency_type(message: Message):
    await message.answer(
        "Виберіть базову валюту для створення графіка",
        reply_markup=get_inline_keyboard(
            btns={
                currency: f"selected_currency:{currency}"
                for currency in SELECTED_CURRENCIES
            },
            sizes=(len(SELECTED_CURRENCIES),),
        ),
    )


@currency_chart_router.callback_query(F.data.startswith("selected_currency:"))
async def get_currency_chart(callback: CallbackQuery):
    currency_type = callback.data.split(":")[1]
    if currency_type not in SELECTED_CURRENCIES:
        await callback.message.answer(
            "Можливо вибрати лише серед наступних валют: "
            + " ".join(i for i in SELECTED_CURRENCIES)
        )
        return
    rates = get_currency_rates(currency_type)
    chart_buf = create_chart(rates, currency_type)
    photo = BufferedInputFile(chart_buf.read(), filename="chart.png")
    await callback.message.answer_photo(photo=photo)
