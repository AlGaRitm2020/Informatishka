import json

import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, message, ParseMode
import logging

import keyboards
import states
from keyboards.default import main_menu
from loader import dp, bot
import utils

@dp.callback_query_handler(state=states.FullVariant.enter_answer)
async def enter_task_number(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if call.data == 'break':
        reply_message = '🔬 Результаты: \n'
        solved, all = 0, len(data['answers'])
        for task_number, answers in data['answers'].items():
            reply_message += f'Задача {task_number}. Ваш ответ: {answers[0]}. Правильный ответ: {answers[1]} \n'
            user_answer = answers[0].lower().replace('\n', ';').replace(' ', '')
            correct_answer = answers[1].lower().replace('\n', ';').replace(' ', '')
            if user_answer == correct_answer:
                solved += 1

            await utils.db_api.add_score(int(task_number), int(user_answer == correct_answer), call.message.chat.id)

        await call.message.answer(reply_message)



        scale_marks = json.load(open('data/practice/scale_marks.json', 'r'))

        await call.message.answer(
            f'ℹ В этом варианте у вас решено правильно {str(solved)} задач из {str(all)}\n'
            f'🟢 *Итоговый балл: {scale_marks[str(solved)]}/100*', parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=keyboards.default.main_menu)

        await call.message.edit_reply_markup(reply_markup=None)

        await state.reset_state(with_data=False)
    else:
        task_number = call.data
        logging.info(f"call = {task_number}")
        await call.answer(cache_time=1)

        task_data = data.get('variant')[int(task_number) - 1]
        task_data['description'] = task_data['description'].replace('"', "")
        message_ids = data.get('message_ids')

        for message_id in message_ids:
            try:
                await bot.delete_message(call.message.chat.id, message_id)
            except Exception:
                logging.info('Message to delete not found')
        message_ids = []

        await call.message.edit_text(f'Вы выбрали задачу под номером {task_number}\n'
                                     f'{task_data["description"]}', reply_markup=keyboards.inline.variant_task_buttons,
                                     parse_mode=ParseMode.MARKDOWN)

        if task_data['image']:
            with open('data/temp_task_files/task.png', 'wb') as img:
                img.write(task_data['image'])
            img = open("data/temp_task_files/task.png", "rb")
            message_obj = await call.message.answer_photo(img)
            message_ids.append(message_obj.message_id)

        if task_data['excel']:
            with open(f'data/temp_task_files/{task_number}_task.xlsx', 'wb') as xlsx:
                xlsx.write(task_data['excel'])
            excel_file = open(f"data/temp_task_files/{task_number}_task.xlsx", "rb")
            message_obj = await call.message.answer_document(excel_file)
            message_ids.append(message_obj.message_id)

        if task_data['word']:
            with open(f'data/temp_task_files/{task_number}_task.docx', 'wb') as docx:
                docx.write(task_data['word'])
            doc_file = open(f"data/temp_task_files/{task_number}_task.docx", "rb")
            message_obj = await call.message.answer_document(task_data['word'])
            message_ids.append(message_obj.message_id)

        if task_data['txt1']:
            with open(f'data/temp_task_files/{task_number}_A_task.txt', 'wb') as txt:
                txt.write(task_data['txt1'])
            txt1_file = open(f"data/temp_task_files/{task_number}_A_task.txt", "rb")
            message_obj = await call.message.answer_document(txt1_file)
            message_ids.append(message_obj.message_id)

        if task_data['txt2']:
            with open(f'data/temp_task_files/{task_number}_B_task.txt', 'wb') as txt:
                txt.write(task_data['txt2'])
            txt2_file = open(f"data/temp_task_files/{task_number}_B_task.txt", "rb")
            message_obj = await call.message.answer_document(txt2_file)
            message_ids.append(message_obj.message_id)

        if 21 >= int(task_number) >= 19:
            message_obj = await call.message.answer(
                '✍️ Напишите ответ на задание. Ответы на каждый из трех вопросов разделите точкой с запятой(;), '
                'а ответы внутри одного вопроса пробелом')
            message_ids.append(message_obj.message_id)
        else:
            message_obj = await call.message.answer(
                '✍️ Напишите ответ на задание. Если ответов несколько, укажите их через пробел')
            message_ids.append(message_obj.message_id)

        await state.update_data(message_ids=message_ids,
                                current_task=task_number)
