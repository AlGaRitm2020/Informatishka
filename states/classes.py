from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateClass(StatesGroup):
    enter_class_name = State()
    enter_teacher_name = State() 
