from aiogram.dispatcher.filters.state import StatesGroup, State


class FullVariant(StatesGroup):
    send_variant = State()
    enter_answer = State()
    get_results = State()