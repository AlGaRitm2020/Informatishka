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
async def create_class_start(message: Message):
    await message.answer(f'Введите имя класса:', reply_markup=keyboards.default.back_menu)
    await states.CreateClass.enter_class_name.set()


@dp.message_handler(text=keyboards.default.class_captions[1], state=None)
async def join_class_start(message: Message):
    await message.answer(f'Введите Id класса:', reply_markup=keyboards.default.back_menu)
    await states.JoinClass.enter_class_id.set()





# --- Create Class Handlers
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
    class_id = str(2)
    
    class_id = await utils.db_api.create_class(class_name, message.chat.id)

    await message.answer(f"Класс '{class_name}' успешно создан \n"
                         f"Id вашего класса: <b>{class_id}</b> \n"
                         f"Отправьте его ученикам, чтобы они присоединились к классу", parse_mode='html')
    await states.finish()



# --- Join Class Handlers

@dp.message_handler(state=states.JoinClass.enter_class_id)
async def enter_class_id(message: Message, state: FSMContext):
    class_id = message.text
    class_ids = ['1', '2']
    if class_id not in class_ids:
        await message.answer("Класс с таким Id не существует\n"
                             "Введите другой Id")
        return False


    class_name = '11A'
    class_teacher = 'Альберт Мансурович'
    await message.answer(f"Вы выбрали класс: {class_name}  \n"
                         f"Учитель: {class_teacher} \n"
                         f"Введите фамилию и имя ( так вас будет видеть учитель)")
    #await utils.db_api.add_feedback(feedback, message.chat.id)
    await state.update_data(class_id=class_id, class_name=class_name)
                            
    await states.JoinClass.next()

@dp.message_handler(state=states.JoinClass.enter_student_name)
async def enter_student_name(message: Message, state: FSMContext):
    student_name = message.text
    
    students_names = ['Альберт']
    if student_name in students_names:
        await message.answer("Ученик с таким именем уже есть в этом классе \n"
                             "Введите другое имя")
        return False

    data = await state.get_data()
    class_id = data.get('class_id')
    class_name = data.get('class_name')
    await message.answer(f"Вы успешно присоединились к классу {class_name} как {student_name}\n")
    #await utils.db_api.add_feedback(feedback, message.chat.id)
    await states.finish()



