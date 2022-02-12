from aiogram.dispatcher.filters.state import StatesGroup, State


class ClassMenu(StatesGroup):
    enter_class = State()
    class_menu = State()
    specific_student = State()
    send_message = State()
    delete_class = State()

class CreateClass(StatesGroup):
    enter_class_name = State()
    enter_teacher_name = State()

class JoinClass(StatesGroup):
    enter_class_id = State()
    enter_student_name = State()

