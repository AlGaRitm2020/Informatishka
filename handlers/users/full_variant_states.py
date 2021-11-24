import asyncio
import logging
import random

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

import parsing
import keyboards
import states
from loader import dp



@dp.message_handler(state=states.FullVariant.send_variant)
async def send_variant(message: Message, state: FSMContext):
    var_number = message.text
    try:
        if var_number == keyboards.default.skip_captions[0]:
            # random variant
            var_number = random.randint(1, 5000)
        elif int(var_number) < 0:
            raise ValueError

        variant = await parsing.generate_random_variant(var_number)
        # putting variant to state storage
        await state.update_data(variant=variant)

        await message.answer(f"🎉 Вариант №{var_number} успешно сгенерирован \n",
                             reply_markup=ReplyKeyboardRemove())
        await message.answer(
            f"Выберите задачу которую хотите решить \n",

            reply_markup=keyboards.inline.variant_task_buttons)
        await states.FullVariant.next()
    except ValueError:
        # if variant number not valid
        await message.answer("⚠ Номер варианта - целое число от 1")
        await states.FullVariant.send_variant.set()




@dp.message_handler(state=states.FullVariant.enter_answer)
async def enter_answer(message: Message, state: FSMContext):
    # getting task data from state vars
    answer = message.text
    # answer.strip()

    data = await state.get_data()
    #variant = data.get('variant')




    # await state.update_data(answer=answer)

    await message.answer(f'Ваш ответ сохранен')
    await state.finish()
