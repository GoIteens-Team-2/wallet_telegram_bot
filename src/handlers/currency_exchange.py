import os
import json
from aiogram import types, Router
from datetime import datetime
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

currency_exchange_router = Router()

user_data = {}

class Form(StatesGroup):
    waiting_for_currency_from = State()
    waiting_for_amount = State()
    waiting_for_currency_to = State()

class CurrencyExchangeState(State):
    main_menu = State()
    select_currency = State()
    input_amount = State()


exchange_rates = {
    'UAH': 1,
    'PLN': 0.22,
    'USD': 0.036,
    'EUR': 0.034,
}

@currency_exchange_router.message_handler(commands=['currencyExchange'])
async def currency_exchange(message: types.Message, state: FSMContext):
    await CurrencyExchangeState.main_menu.set()
    await message.reply("Оберіть операцію:\n1. Конвертувати свій баланс\n2. Інші операції", reply_markup=types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton("Конвертувати свій баланс")],
            [types.KeyboardButton("Інші операції")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    ))

@currency_exchange_router.message_handler(state=CurrencyExchangeState.main_menu)
async def main_menu_handler(message: types.Message, state: FSMContext):
    if message.text == "Конвертувати свій баланс":
        await CurrencyExchangeState.select_currency.set()
        await message.reply("У яку валюту ви хочете конвертувати? (UAH, PLN, USD, EUR)")
    elif message.text == "Інші операції":
        await message.reply("Ця функція ще в розробці.")
    else:
        await message.reply("Невірний вибір. Спробуйте ще раз.")

@currency_exchange_router.message_handler(state=CurrencyExchangeState.select_currency)
async def select_currency_handler(message: types.Message, state: FSMContext):
    if message.text.upper() in exchange_rates:
        await state.update_data(to_currency=message.text.upper())
        await CurrencyExchangeState.input_amount.set()
        await message.reply("Введіть суму для конвертації:")
    else:
        await message.reply("Неправильна валюта. Спробуйте ще раз.")

@currency_exchange_router.message_handler(state=CurrencyExchangeState.input_amount)
async def input_amount_handler(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        data = await state.get_data()
        to_currency = data['to_currency']


        converted_amount = amount * exchange_rates[to_currency] / exchange_rates['UAH']
        await message.reply(f"{amount} UAH = {converted_amount:.2f} {to_currency}")
    except ValueError:
        await message.reply("Будь ласка, введіть правильну суму.")
    finally:
        await state.finish()