import json

from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters import Command

from data.config import ADMINS


from loader import dp
import keyboards
import states
import utils

@dp.message_handler(state=states.Feedback.write_feedback)
async def write_feedback(message: Message, state: FSMContext):
    feedback = message.text
    
    await message.answer("Спасибо за отзыв!")
    await utils.db_api.add_feedback(feedback, message.chat.id)
    await state.finish()



@dp.message_handler(Command('show_feedbacks'))
async def show_feedbacks(message: Message, state: FSMContext):
    if str(message.chat.id) in ADMINS:
        
        
        feedbacks = await utils.db_api.get_feedbacks()
        print(feedbacks)
        reply_message = "Список всех отзывов\n\n"
        for feedback, date, username in feedbacks:
            reply_message += f"Дата:{date.day}.{date.month}.{date.year}\n" \
                             f"Пользователь: {username}\n" \
                             f"Отзыв: {feedback} \n\n"
        await message.answer(reply_message)
        #await utils.db_api.add_feedback(feedback, message.chat.id)
        await state.finish()
    else:
        await message.answer("Access denied! Only for admins!")
    await state.finish()
