from aiogram.dispatcher.filters.state import StatesGroup, State


class TimeStats(StatesGroup):
    enter_number = State()
