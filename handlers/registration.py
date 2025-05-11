from aiogram import Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.db import async_session, User
from sqlalchemy import select
import secrets
import string

router = Router()

class Registration(StatesGroup):
    choosing_role = State()
    entering_tutor_code = State()

@router.message(Command("start"))
async def start_registration(message: types.Message, state: FSMContext):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.userid == message.from_user.id))
        user = result.scalar_one_or_none()
        if user:
            await message.answer("Вы уже зарегистрированы!")
            return
    # Предложить выбрать роль    
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Преподаватель", callback_data="role_teacher")],
            [InlineKeyboardButton(text="Слушатель", callback_data="role_student")]
        ]
    )
    await message.answer("Выберите тип пользователя:", reply_markup=kb)
    await state.set_state(Registration.choosing_role)

# Генерация уникального кода преподавателя
async def generate_unique_tutor_code(session):
    alphabet = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(secrets.choice(alphabet) for _ in range(6))
        result = await session.execute(select(User).where(User.tutrocode == code))
        if not result.scalar_one_or_none():
            return code

@router.callback_query(lambda c: c.data in ["role_teacher", "role_student"]) 
async def process_role_callback(callback: types.CallbackQuery, state: FSMContext):
    role = callback.data
    if role == "role_teacher":
        async with async_session() as session:
            tutor_code = await generate_unique_tutor_code(session)
            # Сохраняем пользователя
            user = User(userid=callback.from_user.id, username=callback.from_user.username or "", role="teacher", tutrocode=tutor_code)
            session.add(user)
            await session.commit()
        await callback.message.edit_text(f"Вы зарегистрированы как преподаватель! Ваш код для студентов: {tutor_code}")
        await state.clear()
    elif role == "role_student":
        await callback.message.edit_text("Введите код преподавателя, который вы получили:")
        await state.set_state(Registration.entering_tutor_code)

@router.message(Registration.entering_tutor_code)
async def process_tutor_code(message: types.Message, state: FSMContext):
    tutor_code = message.text.strip()
    # Проверяем, есть ли такой преподаватель
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tutrocode == tutor_code, User.role == "teacher"))
        teacher = result.scalar_one_or_none()
        if not teacher:
            await message.answer("Код преподавателя не найден. Попробуйте еще раз или обратитесь к преподавателю.")
            return
        # Сохраняем слушателя
        user = User(userid=message.from_user.id, username=message.from_user.username or "", role="student", subscribe=teacher.username)
        session.add(user)
        await session.commit()
    await message.answer(f"Вы зарегистрированы как слушатель преподавателя @{teacher.username}!", reply_markup=types.ReplyKeyboardRemove())
    await state.clear() 