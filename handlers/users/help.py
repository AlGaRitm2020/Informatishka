from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp


@dp.message_handler(Command('help'))
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку")
    await message.answer("\n".join(text))
