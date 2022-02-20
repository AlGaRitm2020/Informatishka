from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

works_captions = ['📎 Создать задание', '⬅ Назад']

works_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=works_captions[0]),
            KeyboardButton(text=works_captions[1])

        ]


        ],
    resize_keyboard=True
)


