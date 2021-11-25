from aiogram import executor

from loader import dp
import middlewares, filters, handlers, diagrams, parsing
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils import db_api

async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

