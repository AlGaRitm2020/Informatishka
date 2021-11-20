from aiogram.types import CallbackQuery
import logging
from loader import dp


@dp.callback_query_handler()
async def enter_task_number(call: CallbackQuery):
    await call.answer(cache_time=1)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    if callback_data == 'break':
        await call.message.answer(f'Вы завершили решение варианта')
    else:
        await call.message.answer(f'Вы выбрали задачу под номером {callback_data}')