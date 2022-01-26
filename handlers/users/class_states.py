import json

from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters import Command

from data.config import ADMINS


from loader import dp
import keyboards
import states
import utils







from loader import dp
from aiogram.types import Message, ReplyKeyboardRemove, ParseMode




# --- class Menu Handlers
@dp.message_handler(text=keyboards.default.class_captions[0], state=None)
async def solve_tasks(message: Message):
    await message.answer(f'Введите имя класса:', reply_markup=keyboards.default.back_menu)
    await states.CreateClass.enter_class_name.set()


@dp.message_handler(text=keyboards.default.main_captions[1], state=None)
async def theory(message: Message):
    await message.answer(f'Вы открыли раздел с теорией \n'
                         f'Введите номер задачи (от 1 до 27)', reply_markup=keyboards.default.back_menu)
    await states.Theory.enter_number.set()






@dp.message_handler(state=states.CreateClass.enter_class_name)
async def enter_class_name(message: Message, state: FSMContext):
    class_name = message.text
    
    await message.answer("Введите свое имя и отчество \n"
                         "Так вас будут видеть ученики")
    #await utils.db_api.add_feedback(feedback, message.chat.id)
    await state.update_data(class_name=class_name)
                            
    await states.CreateClass.next()

@dp.message_handler(state=states.CreateClass.enter_teacher_name)
async def enter_teacher_name(message: Message, state: FSMContext):
    teacher_name = message.text

    data = await state.get_data()
    class_name = data.get('class_name')
    class_id = str(1)
    await message.answer(f"Класс '{class_name}' успешно создан \n"
                         f"Id вашего класса: <b>{class_id}</b> \n"
                         f"Отправьте его ученикам, чтобы они присоединились к классу", parse_mode='html')
    #await utils.db_api.add_feedback(feedback, message.chat.id)
    await states.CreateClass.next()


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
