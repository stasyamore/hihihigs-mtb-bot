# version: 0.1.0
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TOKEN

#экземпляр бота и диспетчера
bot = Bot(token= TOKEN)
dp = Dispatcher()

#Обработчик команды /start
@dp.message(Command(commands=["start"]))
async def process_start_command(message: types.Message):
    await message.answer("Привет!")

#Обработчик текстовых сообщений
@dp.message()
async def echo_message(message: types.Message):
    await message.answer(message.text)

async def main():
    await dp.start_polling(bot)

if __name__ == "main":
    asyncio.run(main())