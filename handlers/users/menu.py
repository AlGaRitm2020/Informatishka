from loader import dp
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.default import main_menu, stat_menu
from aiogram.dispatcher.filters import Command
from keyboards.default import main_captions, stat_captions
from keyboards.inline import variant_task_buttons


@dp.message_handler(text=main_captions[0])
async def solve_tasks(message: Message):
    await message.answer(f'Вы нажали на команду решать задачи', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text=main_captions[2])
async def generate_variant(message: Message):
    await message.answer(f'Вы нажали на команду сгенерировать вариант', reply_markup=variant_task_buttons)


@dp.message_handler(text=main_captions[3])
async def statistics_page(message: Message):
    await message.answer(f'Вы перешли в раздел статистика', reply_markup=stat_menu)

@dp.message_handler(text=stat_captions[3])
async def back_to_home(message: Message):
    await message.answer(f'Вы вернулись на главную страницу', reply_markup=main_menu)
