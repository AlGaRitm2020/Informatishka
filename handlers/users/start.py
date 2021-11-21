from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default import main_menu, main_captions
from loader import dp


@dp.message_handler(Command('start'))
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!",
                         reply_markup=main_menu)


