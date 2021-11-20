from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

stat_captions = ['📎 По всем задачам', '📌 По конкретной задаче', '↗ Активность', '⬅ Назад']

stat_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=stat_captions[0]),
            KeyboardButton(text=stat_captions[1])
        ],
[
            KeyboardButton(text=stat_captions[2]),
            KeyboardButton(text=stat_captions[3])

        ]],
    resize_keyboard=True
)


