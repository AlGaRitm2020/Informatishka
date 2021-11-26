from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_captions = ["🗒 Решать задачи", "📖 Изучать теорию", "📝 Решить целый вариант", "📊 Посмотреть статисктику"]

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=main_captions[0]),
            KeyboardButton(text=main_captions[1]),
            KeyboardButton(text=main_captions[2])
        ],
[
            KeyboardButton(text=main_captions[3])

        ]],
    resize_keyboard=True
)


