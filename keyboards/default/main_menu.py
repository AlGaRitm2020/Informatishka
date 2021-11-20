from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🗒 Решать задачи"),
            KeyboardButton(text="📖 Изучать теорию"),
            KeyboardButton(text="📝 Решить целый вариант")
        ],
[
            KeyboardButton(text="📊 Посмотреть статисктику"),
            KeyboardButton(text="/stop")

        ]],
    resize_keyboard=True
)


