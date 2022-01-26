from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class_captions = ['📎 Создать класс', '📌 Присоедениться к классу', '⬅ Назад']

class_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=class_captions[0]),
            KeyboardButton(text=class_captions[1])
        ],
[
            KeyboardButton(text=class_captions[2]),

        ]],
    resize_keyboard=True
)


