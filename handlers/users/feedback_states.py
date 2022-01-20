import json

from aiogram.dispatcher import FSMContext
from aiogram.types import Message


from loader import dp
import keyboards
import states


@dp.message_handler(state=states.Feedback.write_feedback)
async def write_feedback(message: Message, state: FSMContext):
    feedback = message.text
    
    await message.answer("Спасибо за отзыв!")
    await state.finish()

