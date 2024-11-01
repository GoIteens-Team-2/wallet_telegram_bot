from aiogram import Router
from aiogram.fsm.state import StatesGroup, State

currency_exchange_router = Router()

user_data = {}

class Form(StatesGroup):
    waiting_for_currency_from = State()
    waiting_for_amount = State()
    waiting_for_currency_to = State()

