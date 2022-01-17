from aiogram.dispatcher import FSMContext
from aiogram.types import Message

import diagrams
import keyboards
import states
import utils
from loader import dp


@dp.message_handler(state=states.SpecificTaskStats.enter_number)
async def enter_number(message: Message, state: FSMContext):
    task_number = message.text
    try:
        if int(task_number) < 1 or int(task_number) > 27:
            raise ValueError

        one_task_stats = await utils.db_api.get_stats(message.chat.id, task_number=task_number)
        if not one_task_stats:
            await message.answer(
                f"Вы пока не решали задачу {task_number}.",
                reply_markup=keyboards.default.main_menu)
            await state.finish()

        for task_number, answers in one_task_stats.items():
            correctness = int(answers[0] / answers[1] * 100)
            if correctness > 90:
                result = 'Отличный результат. Продолжай в том же духе.'
            elif correctness > 75:
                result = 'Хороший результат. У тебя все получиться!'
            elif correctness > 50:
                result = 'Есть, над чем работать, но в целом неплохо'
            else:
                result = 'Рекомендую тебе почитать теорию по этой задаче'

            #stat_diagram = await diagrams.get_task_stats_diagram(task_number, answers[0], answers[1], result)
            min_time = 347
            max_time = 507
            avg_time = 304
            recomend_time = 300
            stat_diagram = await diagrams.get_time_stats_diagram(task_number, min_time, max_time, avg_time, recomend_time)
            await message.answer_photo(stat_diagram, reply_markup=keyboards.default.main_menu)

        await state.finish()

    except ValueError:
        "if task_number isn't int"
        await message.answer("⚠ Номер задания - целое число от 1 до 27, попробуй еще раз")
        await states.SpecificTaskStats.enter_number.set()
# fasdgdfsgsdfgdsfg