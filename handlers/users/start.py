from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default import main_menu, main_captions
from loader import dp
from utils import db_api

@dp.message_handler(Command('start'), state="*")
async def bot_start(message: types.Message):
    await db_api.repo.register(message.from_user.username, message.chat.id)
    await message.answer(f"Привет, {message.from_user.full_name}!",
                         reply_markup=main_menu)


