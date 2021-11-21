from aiogram.dispatcher import FSMContext

from loader import dp
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.default import main_menu, stat_menu, back_captions, back_menu
from aiogram.dispatcher.filters import Command
from keyboards.default import main_captions, stat_captions
from keyboards.inline import variant_task_buttons
from states.solve_task import SolveTask
from states.theory import Theory


# --- Main Menu Handlers
@dp.message_handler(text=main_captions[0], state=None)
async def solve_tasks(message: Message):
    await message.answer(f'Вы выбрали режим решения задач ЕГЭ \n'
                         f'Введите номер задачи (от 1 до 27)', reply_markup=back_menu)
    await SolveTask.enter_number.set()


@dp.message_handler(text=main_captions[1], state=None)
async def theory(message: Message):
    await message.answer(f'Вы открыли раздел с теорией \n'
                         f'Введите номер задачи (от 1 до 27)', reply_markup=back_menu)
    await Theory.enter_number.set()


@dp.message_handler(text=main_captions[2])
async def generate_variant(message: Message):
    await message.answer(f'Вы нажали на команду сгенерировать вариант', reply_markup=variant_task_buttons)


@dp.message_handler(text=main_captions[3])
async def statistics_page(message: Message):
    await message.answer(f'Вы перешли в раздел статистика', reply_markup=stat_menu)


# ---


# --- Statistics Menu Handlers
@dp.message_handler(text=stat_captions[3])
async def back_to_home(message: Message):
    await message.answer(f'Вы вернулись на главную страницу', reply_markup=main_menu)


# ---


# Back Menu Handlers ---
@dp.message_handler(state='*', text=back_captions[0])
async def cancel_dialog(message: Message, state: FSMContext):
    await message.answer(f'Вы вернулись в главное меню', reply_markup=main_menu)
    await state.finish()
