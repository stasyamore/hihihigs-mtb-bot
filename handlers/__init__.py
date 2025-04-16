from .handlers import router as message_router
from .bot_commands import set_my_commands
from .callbacks import router as callback_router

def register_message_handlers(dp):
    dp.include_router(message_router)
    dp.include_router(callback_router)

all = ["register_message_handlers", "set_my_commands"]