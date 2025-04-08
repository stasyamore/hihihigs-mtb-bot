from aiogram import Bot
from aiogram.types import BotCommand

async def set_my_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Начать"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="status", description="Статус")
    ]
    await bot.set_my_commands(commands)