import asyncio
import logging
import random

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

import parsing
import keyboards
import states
from loader import dp, bot


@dp.message_handler(state=states.FullVariant.send_variant)
async def send_variant(message: Message, state: FSMContext):

    var_number = message.text
    try:
        if var_number == keyboards.default.skip_captions[0]:
            # random variant
            var_number = random.randint(1, 5000)
        elif int(var_number) < 0 or int(var_number) > 10000:
            raise ValueError

        variant = await parsing.generate_random_variant(var_number)
        # putting variant to state storage
        await state.update_data(variant=variant, message_ids=[], current_task=0, main_message_id=None)

        await message.answer(f"🎉 Вариант №{var_number} успешно сгенерирован \n",
                             reply_markup=ReplyKeyboardRemove())
        message_obj = await message.answer(
            f"Выберите задачу которую хотите решить \n",

            reply_markup=keyboards.inline.variant_task_buttons)
        main_message_id = message_obj.message_id

        # putting variant to state storage
        await state.update_data(variant=variant, message_ids=[], current_task=0,
                                main_message_id=main_message_id, answers=dict())
        await states.FullVariant.next()
    except ValueError:
        # if variant number not valid
        await message.answer("⚠ Номер варианта - целое число от 1 до 10000")
        await states.FullVariant.send_variant.set()


@dp.message_handler(state=states.FullVariant.enter_answer)
async def enter_answer(message: Message, state: FSMContext):
    # getting task data from state vars
    answer = message.text
    answer.strip()

    data = await state.get_data()
    variant = data.get('variant')
    message_ids = data.get('message_ids')
    main_message_id = data.get('main_message_id')
    current_task = data.get('current_task')
    print(data['current_task'])
    data['answers'][data['current_task']] = answer, variant[int(current_task) - 1]['answer']

    for message_id in message_ids:
        try:
            await bot.delete_message(message.chat.id, message_id)
        except Exception:
            logging.info('Message to delete not found')
    await bot.delete_message(message.chat.id, main_message_id)

    message_obj = await message.answer(f'Ваш ответ сохранен', reply_markup=keyboards.inline.variant_task_buttons)
    await state.update_data(message_ids=[], main_message_id=message_obj.message_id,
                            answers=data['answers'])
    await states.FullVariant.enter_answer.set()
