import json

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from keyboards.default import main_menu
from loader import dp
from states.theory import Theory


@dp.message_handler(state=Theory.enter_number)
async def enter_number(message: Message, state: FSMContext):
    task_number = message.text
    try:
        if int(task_number) < 1 or int(task_number) > 27:
            raise ValueError

        theory_links = json.load(open('data/theory/theory_links.json', 'r'))
        videos_links = json.load(open('data/theory/videos_links.json', 'r') )

        await message.answer(f'Задача №{str(task_number)}\n'
                             f'🎬 По этой теме можешь посмотреть видео:\n'
                             f'{videos_links[task_number]}\n'
                             f'📕 Или почитать теорию на сайте:\n'
                             f'{theory_links[task_number]}', reply_markup=main_menu)
        await state.finish()

    except ValueError:
        "if task_number isn't int"
        await message.answer("⚠ Номер задания - целое число от 1 до 27, попробуй еще раз")
        await Theory.enter_number.set()
