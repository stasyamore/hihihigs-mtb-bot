from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# Кнопка с callback-данными
@router.message(Command("info"))
async def send_info_with_buttons(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
        ]
    )
    await message.answer("Это краткая информация.", reply_markup=keyboard)

# Обработка callback
@router.callback_query(lambda call: call.data == "show_more")
async def handle_show_more(callback: types.CallbackQuery):
    await callback.message.edit_text("Вот дополнительная информация!")
    await callback.answer()