from aiogram.dispatcher import FSMContext
from aiogram.types import Message

import keyboards
import states
from loader import dp


@dp.message_handler(state=states.SpecificTaskStats.enter_number)
async def enter_number(message: Message, state: FSMContext):
    task_number = message.text
    try:
        if int(task_number) < 1 or int(task_number) > 27:
            raise ValueError

        await message.answer(f'Статистика по задаче {task_number}', reply_markup=keyboards.default.main_menu)
        await state.finish()

    except ValueError:
        "if task_number isn't int"
        await message.answer("⚠ Номер задания - целое число от 1 до 27, попробуй еще раз")
        await states.SpecificTaskStats.enter_number.set()
