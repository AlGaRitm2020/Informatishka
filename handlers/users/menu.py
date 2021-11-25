from aiogram.dispatcher import FSMContext

from handlers.users.full_variant_states import send_variant
from loader import dp
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.dispatcher.filters import Command

import states
import parsing
import keyboards


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
    await message.answer('Выбирете номер варианта (натуральное число):', reply_markup=keyboards.default.skip_menu)

    print('fasdf')
    await states.FullVariant.send_variant.set()



@dp.message_handler(text=keyboards.default.main_captions[3])
async def statistics_page(message: Message):
    await message.answer(f'Вы перешли в раздел статистика', reply_markup=keyboards.default.stat_menu)


# ---


# --- Statistics Menu Handlers
@dp.message_handler(text=keyboards.default.stat_captions[3])
async def back_to_home(message: Message):
    await message.answer(f'Вы вернулись на главную страницу', reply_markup=keyboards.default.main_menu)

@dp.message_handler(text=keyboards.default.stat_captions[1])
async def back_to_home(message: Message):

    await message.answer(f'Введите номер задачи (от 1 до 27), чтобы посмотреть ее статистику',
                         reply_markup=keyboards.default.back_menu)

    await states.SpecificTaskStats.enter_number.set()

# ---


# Back Menu Handlers ---
@dp.message_handler(state='*', text=keyboards.default.back_captions[0])
async def cancel_dialog(message: Message, state: FSMContext):
    await message.answer(f'Вы вернулись в главное меню', reply_markup=keyboards.default.main_menu)
    await state.finish()
