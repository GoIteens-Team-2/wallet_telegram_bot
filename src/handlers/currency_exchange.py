import os
import requests
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

currency_exchange_router = Router()

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

dp = Dispatcher(storage=MemoryStorage())

def get_exchange_rates():
    response = requests.get(API_URL)
    return response.json()["rates"]

class ConversionState(StatesGroup):
    amount = State()
    from_currency = State()
    to_currency = State()

def currency_keyboard():
    rates = get_exchange_rates()
    builder = ReplyKeyboardBuilder()
    for currency in rates.keys():
        builder.button(text=currency)
    builder.adjust(3) 
    return builder.as_markup(resize_keyboard=True)

@dp.message(ConversionState.amount)
async def process_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
        await state.update_data(amount=amount)
        await message.answer("Оберіть валюту, з якої конвертувати:", reply_markup=currency_keyboard())
        await state.set_state(ConversionState.from_currency)
    except ValueError:
        await message.answer("Будь ласка, введіть правильну числову суму.")

@dp.message(ConversionState.from_currency)
async def process_from_currency(message: Message, state: FSMContext):
    rates = get_exchange_rates()
    if message.text in rates:
        await state.update_data(from_currency=message.text)
        await message.answer("Оберіть валюту, в яку конвертувати:", reply_markup=currency_keyboard())
        await state.set_state(ConversionState.to_currency)
    else:
        await message.answer("Будь ласка, оберіть доступну валюту.")

@dp.message(ConversionState.to_currency)
async def process_to_currency(message: Message, state: FSMContext):
    rates = get_exchange_rates()
    if message.text in rates:
        data = await state.get_data()
        from_currency = data["from_currency"]
        amount = data["amount"]
        to_currency = message.text

        converted_amount = (amount / rates[from_currency]) * rates[to_currency]
        result = f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}"
        await message.answer(result, reply_markup=types.ReplyKeyboardRemove())
        
        await state.clear()
    else:
        await message.answer("Будь ласка, оберіть доступну валюту.")