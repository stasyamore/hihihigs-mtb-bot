import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import register_message_handlers, set_my_commands

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='bot.log',  # файл для логов
    filemode='a',  # режим добавления (append)
)

logger = logging.getLogger(__name__)

async def main():
    """
    Основная функция для установки конфигурации бота.
    Для создания бота необходимо получить token в telegram https://t.me/BotFather
    и добавить полученный токен в файл .env
    """
    logger.info("Запуск бота")

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Регистрация хендлеров
    register_message_handlers()
    logger.info("Хендлеры зарегистрированы")

    # Установка команд
    set_my_commands()
    logger.info("Команды бота установлены")

    # Запуск polling
    logger.info("Запуск polling")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception(f"Ошибка при запуске бота: {e}")