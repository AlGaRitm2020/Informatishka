from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

student_menu_captions = ['📋 Список класса', '📌 Задания', '📌 Написать учителю','❌ Покинуть класс', '⬅ Назад в главное меню']

student_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=student_menu_captions[0]),
            KeyboardButton(text=student_menu_captions[1]),
            KeyboardButton(text=student_menu_captions[2])

        ],
        [
            KeyboardButton(text=student_menu_captions[3]),
            KeyboardButton(text=student_menu_captions[4])
        ]


        ],
    resize_keyboard=True
)

teacher_menu_captions = ['📋 Список учеников', '📌 Задания','❌ Удалить класс', '⬅ Назад в главное меню']

teacher_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=teacher_menu_captions[0]),
            KeyboardButton(text=teacher_menu_captions[1]),
            KeyboardButton(text=teacher_menu_captions[2])

        ],
        [
            KeyboardButton(text=teacher_menu_captions[3])
        ]


        ],
    resize_keyboard=True
)
