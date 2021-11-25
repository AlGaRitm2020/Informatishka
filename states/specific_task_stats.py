from aiogram.dispatcher.filters.state import StatesGroup, State


class SpecificTaskStats(StatesGroup):
    enter_number = State()