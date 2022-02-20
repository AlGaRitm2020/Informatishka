from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

specific_work_teacher_captions = ['✉ Информация о работе', 'Закрыть работу для решения', '❌ Удалить работу', '⬅ Назад в главное меню']

specific_work_teacher_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=specific_work_teacher_captions[0]),
            KeyboardButton(text=specific_work_teacher_captions[1])
        ],

        [
            KeyboardButton(text=specific_work_teacher_captions[2]),
            KeyboardButton(text=specific_work_teacher_captions[3])

        ]


        ],
    resize_keyboard=True
)



specific_work_student_captions = ['✉ Информация о работе', '⬅ Назад в главное меню']

specific_work_student_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=specific_work_student_captions[0]),
            KeyboardButton(text=specific_work_student_captions[1])        ]


        ],
    resize_keyboard=True
)
