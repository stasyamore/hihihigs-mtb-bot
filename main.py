from aiogram import Bot, Dispatcher, Router, types
import asyncio
from aiogram.filters import Command
from keyboard import keyboard
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

@router.message(Command(commands=["start"]))
async def process_start_command(message: types.Message):
    await message.answer("Привет!", reply_markup=keyboard)

@router.message()
async def echo_message(message: types.Message):
    await message.answer(message.text)

dp.include_router(router)

async def main():
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        # Gracefully shut down the bot if Ctrl+C is pressed
        logging.warning("Bot stopped!")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())