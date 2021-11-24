from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

skip_captions = ['⚄ Случайный вариант']

skip_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=skip_captions[0])

        ]],
    resize_keyboard=True
)