from aiogram import Bot, Dispatcher, Router, types
import asyncio
from aiogram.filters import Command
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

@router.message(Command(commands=["start"]))
async def process_start_command(message: types.Message):
    await message.answer("Привет!")

@router.message()
async def echo_message(message: types.Message):
    await message.answer(message.text)

dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())