from aiogram.fsm.state import StatesGroup, State

class MessageState(StatesGroup):
    first_from_to_form = State()
    second_from_to_form = State()