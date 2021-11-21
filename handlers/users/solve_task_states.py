from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from keyboards.default import main_menu
from loader import dp
from states import SolveTask


@dp.message_handler(state=SolveTask.enter_number)
async def enter_number(message: Message, state: FSMContext):
    # another variant to get state
    # state = dp.current_state(chat=message.chat.id, user=message.from_user.id)

    task_number = message.text
    await state.update_data(task_number=int(task_number))

    await message.answer(f'Задача №{task_number}:\n'
                         f'Lorem ipsum ....')
    await SolveTask.next()



@dp.message_handler(state=SolveTask.enter_answer)
async def enter_answer(message: Message, state: FSMContext):

    data = await state.get_data()
    task_number = data.get('task_number')
    answer = message.text
    await state.update_data(answer=int(answer))

    await message.answer(f'Ваш ответ на задачу {str(task_number)}: {answer}', reply_markup=main_menu)
    await state.reset_state(with_data=False)


