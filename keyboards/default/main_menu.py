from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_captions = ["🗒 Решать задачи", "📖 Изучать теорию","📝 Решить целый вариант", "📊 Посмотреть статисктикy", "🤓 Классы","📝Написать oтзыв"]

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=main_captions[0]),
            KeyboardButton(text=main_captions[1]),
            KeyboardButton(text=main_captions[2])
        ],
[
            KeyboardButton(text=main_captions[3]),
            KeyboardButton(text=main_captions[4]),
            KeyboardButton(text=main_captions[5])


        ]],
    resize_keyboard=True
)


