from aiogram import Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from utils.db import async_session, User
from sqlalchemy import select

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
    kb = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="Преподаватель")], [types.KeyboardButton(text="Слушатель")]],
        resize_keyboard=True
    )
    await message.answer("Выберите тип пользователя:", reply_markup=kb)
    await state.set_state(Registration.choosing_role)

@router.message(Registration.choosing_role)
async def process_role(message: types.Message, state: FSMContext):
    role = message.text.lower()
    if role == "преподаватель":
        # Сохраняем пользователя
        async with async_session() as session:
            user = User(userid=message.from_user.id, username=message.from_user.username or "", role="teacher")
            session.add(user)
            await session.commit()
        await message.answer("Вы зарегистрированы как преподаватель!", reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
    elif role == "слушатель":
        await message.answer("Введите код преподавателя, который вы получили:")
        await state.set_state(Registration.entering_tutor_code)
    else:
        await message.answer("Пожалуйста, выберите 'Преподаватель' или 'Слушатель'.")

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
