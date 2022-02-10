from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

specific_student_captions = ['✉ Отправить сообщение', '❌ Исключить из класса', '⬅ Назад']

specific_student_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=specific_student_captions[0]),
            KeyboardButton(text=specific_student_captions[1]),
            KeyboardButton(text=specific_student_captions[2])

        ]


        ],
    resize_keyboard=True
)
