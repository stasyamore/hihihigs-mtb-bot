from aiogram import types, Router, Dispatcher
from aiogram.filters import Command
from .keyboard import keyboard
from utils.db import async_session, User
from sqlalchemy import select

router = Router()
"""
@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=keyboard)
"""
@router.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("Доступные команды:\n/start\n/help\n/status")

@router.message(Command("status"))
async def status_command(message: types.Message):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.userid == message.from_user.id))
        user = result.scalar_one_or_none()
        if not user:
            await message.answer("Вы не зарегистрированы. Пожалуйста, используйте /start для регистрации.")
            return
        if user.role == "student":
            await message.answer(f"Вы слушатель.\nВаш userid: {user.userid}\nВаш преподаватель: @{user.subscribe}\nВаш username: @{user.username}")
        elif user.role == "teacher":
            await message.answer(f"Вы преподаватель.\nВаш userid: {user.userid}\nВаш код для студентов: {user.tutrocode}\nВаш username: @{user.username}")
        else:
            await message.answer(f"Ваш статус: {user.role}\nUsername: @{user.username}")

def register_message_handlers(dp: Dispatcher):
    dp.include_router(router)
