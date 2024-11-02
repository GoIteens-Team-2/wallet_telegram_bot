from aiogram import types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

currency_exchange_router = Router()


class CurrencyExchangeState(StatesGroup):
    main_menu = State()
    select_currency = State()
    input_amount = State()

exchange_rates = {
    'UAH': 1,
    'PLN': 0.22,
    'USD': 0.036,
    'EUR': 0.034,
}

@currency_exchange_router.message(Command('currencyExchange'))
async def currency_exchange(message: types.Message, state: FSMContext):
    await CurrencyExchangeState.main_menu.set()  # Правильно встановлюємо стан main_menu
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Конвертувати свій баланс")],
            [KeyboardButton(text="Інші операції")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.reply("Оберіть операцію:\n1. Конвертувати свій баланс\n2. Інші операції", reply_markup=keyboard)

@currency_exchange_router.message(StateFilter(CurrencyExchangeState.main_menu))
async def main_menu_handler(message: Message, state: FSMContext):
    await message.reply("1")
    if message.text == "Конвертувати свій баланс":
        await state.set_state(CurrencyExchangeState.select_currency)  # Встановлюємо наступний стан
        await message.reply("У яку валюту ви хочете конвертувати? (UAH, PLN, USD, EUR)")
    elif message.text == "Інші операції":
        await message.reply("Ця функція ще в розробці.")
    else:
        await message.reply("Невірний вибір. Спробуйте ще раз.")

@currency_exchange_router.message(StateFilter(CurrencyExchangeState.select_currency))
async def select_currency_handler(message: Message, state: FSMContext):
    if message.text.upper() in exchange_rates:
        await state.update_data(to_currency=message.text.upper())
        await CurrencyExchangeState.input_amount.set()
        await message.reply("Введіть суму для конвертації:")
    else:
        await message.reply("Неправильна валюта. Спробуйте ще раз.")

@currency_exchange_router.message(StateFilter(CurrencyExchangeState.input_amount))
async def input_amount_handler(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
        data = await state.get_data()
        to_currency = data['to_currency']

        # Розрахунок суми після конвертації
        converted_amount = amount * exchange_rates[to_currency] / exchange_rates['UAH']
        await message.reply(f"{amount} UAH = {converted_amount:.2f} {to_currency}")
    except ValueError:
        await message.reply("Будь ласка, введіть правильну суму.")
    finally:
        # Повернення до початкового стану, а не повне очищення стану
        await CurrencyExchangeState.__init__.set()
