from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from app.core.config import settings
from app.bot.handlers import router


async def setup_bot():
    bot = Bot(token=settings.telegram_bot_token)
    dp = Dispatcher()
    dp.include_router(router)

    await bot.set_my_commands([
        BotCommand(command="token", description="Save your JWT token"),
    ])

    return bot, dp
