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

