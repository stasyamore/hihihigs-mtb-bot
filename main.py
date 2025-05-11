
import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import register_message_handlers, set_my_commands
from utils import setup_logger
from utils.db import init_db

async def main():
    """
    Основная функция для установки конфигурации бота.
    Для создания бота необходимо получить token в telegram https://t.me/BotFather
    и добавить полученный токен в файл .env
    """

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Запуск логирования
    setup_logger(fname=__name__)

    # Инициализация базы данных
    await init_db()

    # Регистрация хендлеров
    register_message_handlers(dp)

    # Установка команд
    await set_my_commands(bot)

    # Запуск polling
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
