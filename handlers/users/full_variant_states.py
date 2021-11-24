import asyncio
import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

import parsing
import keyboards
import states
from loader import dp


@dp.message_handler(state=states.FullVariant.send_variant)
async def send_variant(message: Message, state: FSMContext):
    print('full')
    await message.answer('⏳ Подождите, вариант генерируется')
    variant = parsing.generate_random_variant()

    await state.update_data(variant=variant)

    await message.answer(
        "🎉 Вариант успешно сгенерирован \n",
        reply_markup=keyboards.inline.variant_task_buttons)

    await states.FullVariant.next()


@dp.message_handler(state=states.FullVariant.enter_answer)
async def enter_answer(message: Message, state: FSMContext):
    print(9)
    # getting task data from state vars
    data = await state.get_data()
    variant = data.get('variant')


    answer = message.text
    answer.strip()

    await state.update_data(answer=answer)

    await message.answer(f'Ваш ответ сохранен')
    await state.finish()
