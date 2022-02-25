import json

from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters import Command

from data.config import ADMINS


from loader import dp, bot
import keyboards
import states
import utils
import parsing

from loader import dp
from aiogram.types import Message, ReplyKeyboardRemove, ParseMode, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from copy import deepcopy

# --- class Menu Handlers
@dp.message_handler(text=keyboards.default.class_captions[0], state=states.ClassMenu.enter_class)
async def create_class_start(message: Message):
    await message.answer(f'Введите имя класса:', reply_markup=keyboards.default.back_menu)
    await states.CreateClass.enter_class_name.set()


@dp.message_handler(text=keyboards.default.class_captions[1], state=states.ClassMenu.enter_class)
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
    
    class_id = await utils.db_api.create_class(class_name, teacher_name, message.chat.id)

    await message.answer(f"Класс '{class_name}' успешно создан \n"
                         f"Id вашего класса: <b>{class_id}</b> \n"
                         f"Отправьте его ученикам, чтобы они присоединились к классу", parse_mode='html')
    await state.finish()



# --- Join Class Handlers

@dp.message_handler(state=states.JoinClass.enter_class_id)
async def enter_class_id(message: Message, state: FSMContext):
    class_id = message.text

    class_info = await utils.db_api.view_class(class_id, message.chat.id)
    if isinstance(class_info, str):
        await message.answer(class_info)
        return False
    else:
        class_name = class_info[0]
        teacher_name = class_info[1]

        await message.answer(f"Вы выбрали класс: {class_name}  \n"
                         f"Учитель: {teacher_name} \n"
                         f"Введите фамилию и имя ( так вас будет видеть учитель)")
        #await utils.db_api.add_feedback(feedback, message.chat.id)
        await state.update_data(class_id=class_id, class_name=class_name)
                            
        await states.JoinClass.next()

@dp.message_handler(state=states.JoinClass.enter_student_name)
async def enter_student_name(message: Message, state: FSMContext):
    student_name = message.text
    

    data = await state.get_data()
    class_id = data.get('class_id')
    class_name = data.get('class_name')

    response = await utils.db_api.join_class(class_id, student_name ,message.chat.id)
    if response:
        await message.answer(response)
        return False
    else:
        await message.answer(f"Вы успешно присоединились к классу {class_name} как {student_name}\n")
        await state.finish()


# --- User Classes Handlers

@dp.message_handler(state=states.ClassMenu.enter_class)
async def enter_class_name(message: Message, state: FSMContext):
    user_classes = await utils.db_api.view_all_user_classes(message.chat.id)
    for class_id, class_name in user_classes:
        if message.text == f"{class_name}({class_id})":

            is_teacher = await utils.db_api.is_teacher(class_id, message.chat.id)
            if is_teacher:
                status = 'учитель'
                reply_keyboard = keyboards.default.teacher_menu
            else:
                status = 'ученик'
                reply_keyboard = keyboards.default.student_menu
            await state.update_data(class_name=class_name, class_id=class_id, is_teacher=is_teacher)
            await message.answer(f"Вы вошли в меню класса {class_name} как {status}", reply_markup=reply_keyboard)
            await states.ClassMenu.next()
            break
    else:
        await message.answer("404: Класс с таким именем и id не найден")



@dp.message_handler(state=states.ClassMenu.class_menu, text=keyboards.default.student_menu_captions[0])
async def print_class_members(message: Message, state: FSMContext):
    data = await state.get_data()
    class_id = data.get('class_id')
    class_name = data.get('class_name')
    members_list = await utils.db_api.view_class_members(class_id)
    
    response = f'<b>Список класса {class_name}</b>\n'
    for i, item in enumerate(members_list):
        name = item[0]
        if i == 0:
            response += f'Учитель: {name}\nУченики:\n'
            
        else:
            response += f'{i}. {name}'

    await message.answer(response, parse_mode='html')



@dp.message_handler(state=states.ClassMenu.class_menu, text=keyboards.default.student_menu_captions[1])
async def works_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    
    class_id = data.get("class_id")
    is_teacher = data.get("is_teacher")
    works_list = await utils.db_api.get_homeworks(class_id)

    if is_teacher:
        reply_markup = deepcopy(keyboards.default.works_menu)
    else:
        reply_markup = deepcopy(keyboards.default.back_menu)
    for id, name, tasks in works_list:
        class_button = KeyboardButton(f"{name}")
        reply_markup = reply_markup.insert(class_button)

    await message.answer("Выберите задание",reply_markup=reply_markup, parse_mode='html')

    await states.ClassMenu.works_menu.set()


@dp.message_handler(state=states.ClassMenu.class_menu, text=keyboards.default.student_menu_captions[3])
async def leave_from_class(message: Message, state: FSMContext):
    data = await state.get_data()
    class_id = data.get('class_id')
    class_name = data.get('class_name')
    
    await utils.db_api.leave_from_class(class_id, message.chat.id)

    await message.answer(f"Вы покинули класс {class_name}")

@dp.message_handler(state=states.ClassMenu.class_menu, text=keyboards.default.teacher_menu_captions[2])
async def approve_deletion(message: Message, state: FSMContext):
    data = await state.get_data()
    class_name = data.get('class_name')
    
    await message.answer(f"Вы точно хотите удалить класс {class_name}? Отменить это действие будет невозможно\n"
                         f"Введите имя класса в качестве подтверждения")
    await states.ClassMenu.delete_class.set()

@dp.message_handler(state=states.ClassMenu.delete_class)
async def delete_class(message: Message, state: FSMContext):
    data = await state.get_data()
    class_id = data.get('class_id')
    class_name = data.get('class_name')
    if message.text == class_name:

        await utils.db_api.delete_class(class_id, message.chat.id)

        await message.answer(f"Класс {class_name} удален")
    else:
        await message.answer(f"Имя класса введено неверно. Отмена операции")
        await state.finish()
        await states.ClassMenu.class_menu.set()
        await state.update_data(class_name=class_name, class_id=class_id)


@dp.message_handler(state=states.ClassMenu.class_menu, text=keyboards.default.teacher_menu_captions[0])
async def print_class_members(message: Message, state: FSMContext):
    data = await state.get_data()
    class_id = data.get('class_id')
    class_name = data.get('class_name')
    members_list = await utils.db_api.view_class_members(class_id, teacher=False)
    
    reply_markup = deepcopy(keyboards.default.back_menu)
    for student_name in members_list:
        class_button = KeyboardButton(f"{student_name[0]}")
        reply_markup = reply_markup.insert(class_button)

    await message.answer("Выберите ученика",reply_markup=reply_markup, parse_mode='html')
    await states.ClassMenu.specific_student.set()


@dp.message_handler(state=states.ClassMenu.works_menu, text=keyboards.default.works_captions[0])
async def create_work(message: Message, state: FSMContext):

    await message.answer("Введите название для новой работы. Постарайтесь сделать его понятным для учеников") 
    await states.ClassMenu.next()


@dp.message_handler(state=states.ClassMenu.works_menu)
async def go_to_specific_work(message: Message, state: FSMContext):
    data = await state.get_data()
    is_teacher = data.get("is_teacher")
    class_id = data.get("class_id")
    works_list = await utils.db_api.get_homeworks(class_id)

    for id, name, tasks in works_list:
        if message.text == name:
            await state.update_data(work_id=id, work_name=name, work_tasks=tasks)
            
            if is_teacher:

            
                await message.answer(f"Вы перешли в меню задания {name}, как учитель",reply_markup=keyboards.default.specific_work_teacher_menu)

            else:
                await message.answer(f"Вы перешли в меню задания {name}",reply_markup=keyboards.default.specific_work_student_menu)

            await states.ClassMenu.specific_work.set()

@dp.message_handler(state=states.ClassMenu.specific_work, text=keyboards.default.specific_work_student_captions[0])
async def work_info(message: Message, state: FSMContext):

    data = await state.get_data()
    class_id = data.get("class_id")
    work_name = data.get("work_name")
    work_id = data.get("work_id")

    tasks = data.get("work_tasks").replace(",",", ")
    try:
        work_info = await utils.db_api.get_work_info(class_id, work_id)
        
        if work_info[1] == 1:
            status = "Открыто для решения"
        else:
            status = "Закрыто для решения"

        await message.answer(f"Задание '{work_name}'\n"\
                             f"Статус: {status}\n"\
                             f"Задачи: {tasks}\n"\
                             f"Дата создания(ГГГГ-ММ-ДД): {work_info[0]}\n")
        await states.ClassMenu.specific_work.set()
    except IndexError:
        await message.answer("Такого задания больше не существует")

@dp.message_handler(state=states.ClassMenu.specific_work, text=keyboards.default.specific_work_student_captions[1])
async def solve_work(message: Message, state: FSMContext):

    data = await state.get_data()
    class_id = data.get("class_id")
    work_name = data.get("work_name")
    
    tasks = data.get("work_tasks").replace(",",", ")


    await message.answer(f"⏳ Задание будет получено через 5-10 секунд  \n",
    reply_markup=ReplyKeyboardRemove()) 
    try:
        tasks_list = tasks.split(",")
        variant = await parsing.get_task_by_id(tasks_list)
        # putting variant to state storage
        
        inline_keyboard = InlineKeyboardMarkup()
        for i, task_id in enumerate(tasks_list):
            inline_keyboard = inline_keyboard.insert(InlineKeyboardButton(text=task_id, callback_data=i))
        inline_keyboard = inline_keyboard.add(InlineKeyboardButton(text="Завершить решение варианта", callback_data="break"))

        await state.update_data(variant=variant, message_ids=[], current_task=0, main_message_id=None, custom_keyboard=inline_keyboard)

        await message.answer(f"🎉 Задание от учителя {work_name} успешно получено \n",
                             reply_markup=ReplyKeyboardRemove())
        message_obj = await message.answer(
            f"Выберите задачу которую хотите решить \n",

            reply_markup=inline_keyboard)
        main_message_id = message_obj.message_id

        # putting variant to state storage
        await state.update_data(variant=variant, message_ids=[], current_task=0,
                                main_message_id=main_message_id, answers=dict(), last_time=None, time_dict=dict())
        await states.FullVariant.enter_answer.set()
    except IndexError:
        await message.answer("Такого задания больше не существует")



@dp.message_handler(state=states.ClassMenu.specific_work, text=keyboards.default.specific_work_teacher_captions[1])
async def change_work_status(message: Message, state: FSMContext):

    data = await state.get_data()
    class_id = data.get("class_id")
    work_name = data.get("work_name")
    work_id = data.get("work_id")

    try:
        updated_status = await utils.db_api.change_work_status(class_id, work_id)
        
        if updated_status == 1:
            status = "открыто для решения"
        else:
            status = "закрыто для решения"

        await message.answer(f"Статус изменен. Теперь задание '{work_name}' {status}\n")
        await states.ClassMenu.specific_work.set()
    except IndexError:
        await message.answer("Такого задания больше не существует")

@dp.message_handler(state=states.ClassMenu.specific_work, text=keyboards.default.specific_work_teacher_captions[2])
async def approve_deletion_work(message: Message, state: FSMContext):

    data = await state.get_data()
    work_name = data.get("work_name")

    await message.answer(f"Вы точно хотите задание {work_name}?\n"
                         f"Введите название задания в качестве подтверждения")
    await states.ClassMenu.delete_work.set()

@dp.message_handler(state=states.ClassMenu.delete_work)
async def delete_work(message: Message, state: FSMContext):
    data = await state.get_data()
    class_id = data.get('class_id')
    work_name = data.get('work_name')
    work_id = data.get('work_id')

    if message.text == work_name:

        await utils.db_api.delete_work(class_id, work_id)

        await message.answer(f"Задание {work_name} удалено", reply_markup=keyboards.default.teacher_menu)
        await states.ClassMenu.class_menu.set()
    else:
        await message.answer(f"Имя работы введено неверно. Отмена операции")
        await state.finish()
        await states.ClassMenu.class_menu.set()
        await state.update_data(class_name=class_name, class_id=class_id)




@dp.message_handler(state=states.ClassMenu.enter_work_name)
async def enter_work_name(message: Message, state: FSMContext):
    work_name = message.text
    await state.update_data(work_name=work_name)

    await message.answer("Введите номера заданий из базы данных Полякова через запятую")
    await states.ClassMenu.next()


@dp.message_handler(state=states.ClassMenu.enter_tasks)
async def enter_tasks(message: Message, state: FSMContext):
    tasks = message.text.replace(' ', '')

    data = await state.get_data()
    work_name = data.get("work_name")
    class_id = data.get("class_id")
    student_name = data.get('student_name')
    class_name = data.get('class_name')
    
    await utils.db_api.create_homework(work_name, class_id, tasks)
    
    class_info = await utils.db_api.view_class(class_id, message.chat.id, read_only=True)
    if isinstance(class_info, str):
        await message.answer(class_info)
        return False
    else:
        teacher_name = class_info[1]


    chat_id_list = await utils.db_api.get_all_students_chat_ids(class_id)
    if chat_id_list:
        for chat_id in chat_id_list:
            chat_id = chat_id[0]

            await bot.send_message(chat_id, f"🔔 Ваш учитель {teacher_name} в классе {class_name} отправил вам задание {work_name}\n"
                               f"Вы можете решить его в меню классы -> задания")
    
    await message.answer("Работа была отправлена вашим ученикам. Они получат уведомление в боте", reply_markup=keyboards.default.teacher_menu)

    await states.ClassMenu.class_menu.set()




@dp.message_handler(state=states.ClassMenu.specific_student, text=keyboards.default.specific_student_captions[0]) 
async def write_message(message: Message, state: FSMContext):
    
    data = await state.get_data()
    student_name = data.get("student_name")

    await message.answer(f"Введите сообщение для ученика {student_name}:")
    await states.ClassMenu.next()

@dp.message_handler(state=states.ClassMenu.specific_student, text=keyboards.default.specific_student_captions[1])
async def approve_deletion(message: Message, state: FSMContext):
    data = await state.get_data()
    student_name = data.get("student_name")

    await message.answer(f"Вы точно хотите исключить ученика {student_name}?\n"
                         f"Введите имя ученика в качестве подтверждения")
    await states.ClassMenu.remove_student.set()

@dp.message_handler(state=states.ClassMenu.specific_student)
async def specific_student(message: Message, state: FSMContext):
    data = await state.get_data()
    class_id = data.get('class_id')

    members_list = await utils.db_api.view_class_members(class_id, teacher=False)
    for student_name in members_list:
        if message.text == student_name[0]:
           
            reply_keyboard = keyboards.default.student_menu
            await state.update_data(student_name=student_name[0])
            await message.answer(f"Выберите действие", reply_markup=keyboards.default.specific_student_menu)
            break
    else:
        await message.answer("404: Ученик с таким именем не найден")







@dp.message_handler(state=states.ClassMenu.send_message) 
async def send_message(message: Message, state: FSMContext):
    data = await state.get_data()

    class_id = data.get('class_id')
    student_name = data.get('student_name')
    class_name = data.get('class_name')
    student_chat_id = int(await utils.db_api.get_student_chat_id(class_id, student_name))
    
    class_info = await utils.db_api.view_class(class_id, message.chat.id, read_only=True)
    if isinstance(class_info, str):
        await message.answer(class_info)
        return False
    else:
        teacher_name = class_info[1]

    message_from_teacher = message.text 

    await bot.send_message(student_chat_id, f"🔔 Ваш учитель {teacher_name} отправил вам сообщение:\n"
                               f"{message_from_teacher}")

    await message.answer("Сообщение успешно отправлено", reply_markup=keyboards.default.teacher_menu)
    await states.ClassMenu.class_menu.set()



@dp.message_handler(state=states.ClassMenu.remove_student)
async def remove_student(message: Message, state: FSMContext):
    data = await state.get_data()
    class_id = data.get('class_id')
    student_name = data.get('student_name')
    class_name = data.get('class_name')


    await message.answer(class_id) 
    if message.text == student_name:

        await utils.db_api.remove_student(class_id, student_name)

        await message.answer(f"Ученик {student_name} исключен", reply_markup=keyboards.default.teacher_menu)

        await states.ClassMenu.class_menu.set()
    else:
        await message.answer(f"Имя ученика введено неверно. Отмена операции", reply_markup=keyboards.default.teacher_menu)
        await state.finish()
        
        await state.update_data(class_name=class_name, class_id=class_id)
        await states.ClassMenu.class_menu.set()
