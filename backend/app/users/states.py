from aiogram.fsm.state import State, StatesGroup

class RegState(StatesGroup):
    username = State()