from aiogram import types, Router, Dispatcher
from aiogram.filters import Command
from .keyboard import keyboard

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=keyboard)

@router.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("Доступные команды:\n/start\n/help\n/status")

@router.message(Command("status"))
async def status_command(message: types.Message):
    await message.answer(f"ID: {message.from_user.id}\nUsername: @{message.from_user.username}")

def register_message_handlers(dp: Dispatcher):
    dp.include_router(router)