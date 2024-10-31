from aiogram.fsm.state import StatesGroup, State

class MessageState(StatesGroup):
    quest_1 = State()
    quest_2 = State()
    analis_answer = State()