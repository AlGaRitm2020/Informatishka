from aiogram.dispatcher.filters.state import StatesGroup, State


class SolveTask(StatesGroup):
    enter_number = State()
    enter_answer = State()