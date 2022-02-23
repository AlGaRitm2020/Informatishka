from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

specific_work_teacher_captions = ['✉ Информация о работе', 'Изменить статус работы', '❌ Удалить работу', '⬅ Назад в главное меню']

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



specific_work_student_captions = ['✉ Информация о работе', 'Приступить к решению', '⬅ Назад в главное меню']

specific_work_student_menu = ReplyKeyboardMarkup(
    keyboard=[
        [ 
            KeyboardButton(text=specific_work_student_captions[0]),
            KeyboardButton(text=specific_work_student_captions[1]),
            KeyboardButton(text=specific_work_student_captions[2])
        ]

        ],
    resize_keyboard=True
)