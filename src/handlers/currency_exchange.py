from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from ..keyboards import get_inline_keyboard
from ..service.data_management import data_manager
from ..constants import SELECTED_CURRENCIES
from ..service.currency import get_currency_rates

currency_exchange_router = Router()


@currency_exchange_router.message(Command("exchange"))
async def currency_exchange(message: Message):
    buttons = {
        "Конвертувати свій баланс у валюту": "exchange_convert_balance",
        # "Переведення з гривні в іншу валюту": "exchange_convert_value",
        "Інші операції": "exchange_others",
    }
    await message.answer(
        "Оберіть операцію:",
        reply_markup=get_inline_keyboard(
            btns=buttons,
            sizes=(1,) * len(buttons),
        ),
    )


@currency_exchange_router.message(Command("exchange_balance"))
@currency_exchange_router.callback_query(F.data == "exchange_convert_balance")
async def exchange_balance(event: Message | CallbackQuery):
    if isinstance(event, CallbackQuery):
        event = event.message

    await event.answer(
        "Виберіть валюту, у якій хочете дізнатися свій баланс:",
        reply_markup=get_inline_keyboard(
            btns={
                currency: f"exchange_currency_balance:{currency}"
                for currency in SELECTED_CURRENCIES
                if currency != "UAH"
            },
            sizes=(len(SELECTED_CURRENCIES),),
        ),
    )


@currency_exchange_router.callback_query(
    F.data.startswith("exchange_currency_balance:")
)
async def get_currency_chart(callback: CallbackQuery):
    user_id = callback.from_user.id

    data_manager.load_user_data(user_id)
    balance = data_manager.user_data[user_id]["balance"]

    currency_type = callback.data.split(":")[1]
    if currency_type not in SELECTED_CURRENCIES:
        await callback.message.answer(
            "Можливо вибрати лише серед наступних валют: "
            + " ".join(i for i in SELECTED_CURRENCIES)
        )
        return

    rates = get_currency_rates("UAH")

    result = balance * rates[currency_type]
    await callback.message.answer(f"Result = {result}")


@currency_exchange_router.message(Command("exchange_others"))
@currency_exchange_router.callback_query(F.data == "exchange_others")
async def exchange_balance(event: Message | CallbackQuery):
    if isinstance(event, CallbackQuery):
        event = event.message

    await event.answer("Більше можливостей буде в майбутньому...")
