from aiogram import Bot, types

async def set_my_commands(bot: Bot):
    commands = [
        types.BotCommand(command="start", description="Запуск бота"),
        types.BotCommand(command="help", description="Справка"),
        types.BotCommand(command="status", description="Показать статус"),
        types.BotCommand(command="info", description="Показать информацию"),
    ]
    await bot.set_my_commands(commands)

