import asyncio
import logging

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from keyboards.default import main_menu
from loader import dp
from parsing.task_by_number import get_task_by_number
from states import SolveTask


@dp.message_handler(state=SolveTask.enter_number)
async def enter_number(message: Message, state: FSMContext):
    # another variant to get state
    # state = dp.current_state(chat=message.chat.id, user=message.from_user.id)

    task_number = message.text
    # print(get_task_by_number(task_number))
    coroutine_task = asyncio.create_task(get_task_by_number(task_number))
    await asyncio.gather(coroutine_task)

    task_text, right_answer, byte_img, byte_excel, byte_word, byte_txt_1, byte_txt_2 = coroutine_task.result()

    await state.update_data(task_number=task_number,
                            task_text=task_text,
                            right_answer=right_answer)

    await message.answer(f'Задание № {task_number}\n' + task_text)

    if byte_img:
        with open('data/temp_task_files/task.png', 'wb') as img:
            img.write(byte_img)
        img = open("data/temp_task_files/task.png", "rb")
        await message.reply_photo(img)

    if byte_excel:
        with open(f'data/temp_task_files/{task_number}_task.xlsx', 'wb') as xlsx:
            xlsx.write(byte_excel)
        excel_file = open(f"data/temp_task_files/{task_number}_task.xlsx", "rb")
        await message.reply_document(excel_file)
    if byte_word:
        with open(f'data/temp_task_files/{task_number}_task.docx', 'wb') as docx:
            docx.write(byte_word)
        doc_file = open(f"data/temp_task_files/{task_number}_task.docx", "rb")
        await message.reply_document(doc_file)
    if byte_txt_1:
        with open(f'data/temp_task_files/{task_number}_A_task.txt', 'wb') as txt:
            txt.write(byte_txt_1)
        txt1_file = open(f"data/temp_task_files/{task_number}_A_task.txt", "rb")
        await message.reply_document(txt1_file)
    if byte_txt_2:
        with open(f'data/temp_task_files/{task_number}_B_task.txt', 'wb') as txt:
            txt.write(byte_txt_2)
        txt2_file = open(f"data/temp_task_files/{task_number}_B_task.txt", "rb")
        await message.reply_document(txt2_file)

    if 21 >= int(task_number) >= 19:
        await message.answer(
            '✍️ Напишите ответ на задание. Ответы на каждый из трех вопросов разделите точкой с запятой(;), '
            'а ответы внутри одного вопроса пробелом')
    else:
        await message.answer('✍️ Напишите ответ на задание. Если ответов несколько, укажите их через пробел')
    await SolveTask.next()


@dp.message_handler(state=SolveTask.enter_answer)
async def enter_answer(message: Message, state: FSMContext):
    # getting task data from state vars
    data = await state.get_data()
    task_number = data.get('task_number')
    right_answer = data.get('right_answer')

    answer = message.text
    await state.update_data(answer=int(answer))

    await message.answer(f'Ваш ответ на задачу {str(task_number)}: {answer}', reply_markup=main_menu)
    await state.reset_state(with_data=False)
