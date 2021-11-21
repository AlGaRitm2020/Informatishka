from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

back_captions = ['⬅ Назад в главное меню']

back_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=back_captions[0])

        ]],
    resize_keyboard=True
)