import json
from aiogram import types, Router
from datetime import datetime
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

currency_exchange_router = Router()

user_data = {}


# class Form(StatesGroup):
#     waiting_for_currency_from = State()
#     waiting_for_amount = State()
#     waiting_for_currency_to = State()


# @currency_exchange_router.message(Command("exchange"))
# async def cmd_exchange(message: types.Message):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     currencies = ["USD", "EUR", "UAH"]
#     for currency in currencies:
#         keyboard.add(currency)
#     await message.answer(
#         "Оберіть валюту, з якої будете переводити гроші:", reply_markup=keyboard
#     )
#     await Form.waiting_for_currency_from.set()


# @currency_exchange_router.message(state=Form.waiting_for_currency_from)
# async def process_currency_from(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data["currency_from"] = message.text
#     await message.answer("Введіть кількість грошей:")
#     await Form.waiting_for_amount.set()


# @currency_exchange_router.message(state=Form.waiting_for_amount)
# async def process_amount(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data["amount"] = message.text
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     currencies = ["USD", "EUR", "UAH"]
#     for currency in currencies:
#         keyboard.add(currency)
#     await message.answer(
#         "Оберіть валюту, в яку будете переводити гроші:", reply_markup=keyboard
#     )
#     await Form.waiting_for_currency_to.set()


# @currency_exchange_router.message(state=Form.waiting_for_currency_to)
# async def process_currency_to(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data["currency_to"] = message.text
#         currency_from = data["currency_from"]
#         amount = data["amount"]
#         currency_to = data["currency_to"]
#     await message.answer(
#         f"Ви обрали перевести {amount} {currency_from} в {currency_to}."
#     )
#     await state.finish()


# @currency_exchange_router.message(Command("exchange"))
# async def cmd_exchange(message: types.Message):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     currencies = ["USD", "EUR", "UAH"]
#     for currency in currencies:
#         keyboard.add(currency)
#     await message.answer(
#         "Оберіть валюту, з якої будете переводити гроші:", reply_markup=keyboard
#     )
#     user_data[message.from_user.id] = {"step": "currency_from"}


# @currency_exchange_router.message(
#     lambda message: user_data.get(message.from_user.id, {}).get("step")
#     == "currency_from"
# )
# async def process_currency_from(message: types.Message):
#     user_data[message.from_user.id]["currency_from"] = message.text
#     await message.answer("Введіть кількість грошей:")
#     user_data[message.from_user.id]["step"] = "amount"


# @currency_exchange_router.message(
#     lambda message: user_data.get(message.from_user.id, {}).get("step") == "amount"
# )
# async def process_amount(message: types.Message):
#     user_data[message.from_user.id]["amount"] = message.text
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     currencies = ["USD", "EUR", "UAH"]
#     for currency in currencies:
#         keyboard.add(currency)
#     await message.answer(
#         "Оберіть валюту, в яку будете переводити гроші:", reply_markup=keyboard
#     )
#     user_data[message.from_user.id]["step"] = "currency_to"


# @currency_exchange_router.message(
#     lambda message: user_data.get(message.from_user.id, {}).get("step") == "currency_to"
# )
# async def process_currency_to(message: types.Message):
#     user_data[message.from_user.id]["currency_to"] = message.text
#     currency_from = user_data[message.from_user.id]["currency_from"]
#     amount = user_data[message.from_user.id]["amount"]
#     currency_to = user_data[message.from_user.id]["currency_to"]
#     user_id = message.from_user.id

#     transaction_data = {
#         "user_id": user_id,
#         "currency_from": currency_from,
#         "amount": amount,
#         "currency_to": currency_to,
#         "timestamp": datetime.now().isoformat(),
#     }

#     filename = f'transactions/transaction_{user_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
#     with open(filename, "w") as json_file:
#         json.dump(transaction_data, json_file, indent=4)

#     await message.answer(
#         f"Ви обрали перевести {amount} {currency_from} в {currency_to}. Транзакцію збережено."
#     )
#     del user_data[message.from_user.id]
