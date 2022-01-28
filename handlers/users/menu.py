from aiogram.dispatcher import FSMContext

import utils
from handlers.users.full_variant_states import send_variant
from loader import dp
from aiogram.types import Message, ReplyKeyboardRemove, ParseMode, KeyboardButton

from aiogram.dispatcher.filters import Command

import states
import parsing
import keyboards
import diagrams
from copy import deepcopy

# --- Main Menu Handlers
@dp.message_handler(text=keyboards.default.main_captions[0], state=None)
async def solve_tasks(message: Message):
    await message.answer(f'Вы выбрали режим решения задач ЕГЭ \n'
                         f'Введите номер задачи (от 1 до 27)', reply_markup=keyboards.default.back_menu)
    await states.SolveTask.enter_number.set()


@dp.message_handler(text=keyboards.default.main_captions[1], state=None)
async def theory(message: Message):
    await message.answer(f'Вы открыли раздел с теорией \n'
                         f'Введите номер задачи (от 1 до 27)', reply_markup=keyboards.default.back_menu)
    await states.Theory.enter_number.set()


@dp.message_handler(text=keyboards.default.main_captions[2], state=None)
async def generate_variant(message: Message, state: FSMContext):
    await message.answer('Выбирете номер варианта (натуральное число до 10000):', reply_markup=keyboards.default.skip_menu)

    await states.FullVariant.send_variant.set()


@dp.message_handler(text=keyboards.default.main_captions[3])
async def statistics_page(message: Message):
    await message.answer(f'Вы перешли в раздел статистика', reply_markup=keyboards.default.stat_menu)

@dp.message_handler(text=keyboards.default.main_captions[4])
async def classes_page(message: Message):
    await message.answer(str(keyboards.default.class_menu))
    classes_info = set(await utils.db_api.view_all_my_classes(message.chat.id))

    reply_markup = deepcopy(keyboards.default.class_menu)
    for class_id, class_name in classes_info:
        class_button = KeyboardButton(f"{class_name}({class_id})")
        reply_markup = reply_markup.insert(class_button)
    await message.answer(f'Вы перешли в раздел классы', reply_markup=reply_markup)
    await message.answer(keyboards.default.class_menu)

@dp.message_handler(text=keyboards.default.main_captions[5])
async def feedback_page(message: Message):
    await message.answer(f'Напишите отзыв', reply_markup=keyboards.default.back_menu)
    await states.Feedback.write_feedback.set()




# ---


# --- Statistics Menu Handlers
@dp.message_handler(text=keyboards.default.stat_captions[3])
async def back_to_home(message: Message):
    await message.answer(f'Вы вернулись на главную страницу', reply_markup=keyboards.default.main_menu)


@dp.message_handler(text=keyboards.default.stat_captions[1])
async def get_specific_task_stats(message: Message):
    await message.answer(f'Введите номер задачи (от 1 до 27), чтобы посмотреть ее статистику',
                         reply_markup=keyboards.default.back_menu)

    await states.SpecificTaskStats.enter_number.set()


@dp.message_handler(text=keyboards.default.stat_captions[4])
async def get_specific_task_stats(message: Message):
    await message.answer(f'Введите номер задачи (от 1 до 27), чтобы посмотреть ее статистику',
                         reply_markup=keyboards.default.back_menu)

    await states.TimeStats.enter_number.set()


@dp.message_handler(text=keyboards.default.stat_captions[0])
async def get_all_tasks_stats(message: Message):
    all_task_stats = await utils.db_api.get_stats(message.chat.id)
    if not all_task_stats:
        await message.answer("Вы пока не решали задачи",
                             reply_markup=keyboards.default.main_menu)

    for task_number, answers in all_task_stats.items():
        correctness = int(answers[0] / answers[1] * 100)
        if correctness > 90:
            result = 'Отличный результат. Продолжай в том же духе.'
        elif correctness > 75:
            result = 'Хороший результат. У тебя все получиться!'
        elif correctness > 50:
            result = 'Есть, над чем работать, но в целом неплохо'
        else:
            result = 'Рекомендую тебе почитать теорию по этой задаче'

        stat_diagram = await diagrams.get_task_stats_diagram(task_number, answers[0], answers[1], result)
        await message.answer_photo(stat_diagram, reply_markup=keyboards.default.main_menu)


@dp.message_handler(text=keyboards.default.stat_captions[2])
async def get_activity_stats(message: Message):
    activity_stats = await utils.db_api.repo.get_activity(message.chat.id)

    if not activity_stats:
        await message.answer("Вы еще не решали задачи", reply_markup=keyboards.default.main_menu)
    diagram = await diagrams.get_user_activity_diagram(activity_stats)
    await message.answer_photo(diagram, reply_markup=keyboards.default.main_menu)


# ---


# Back Menu Handlers ---
@dp.message_handler(state='*', text=keyboards.default.back_captions[0])
async def cancel_dialog(message: Message, state: FSMContext):
    await message.answer(f'Вы вернулись в главное меню', reply_markup=keyboards.default.main_menu)
    await state.finish()
