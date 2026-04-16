from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.session.aiohttp import AiohttpSession
from app.core.config import settings
from app.bot.handlers import router


async def setup_bot():
    session = None
    if settings.proxy_url:
        session = AiohttpSession(proxy=settings.proxy_url)

    bot = Bot(token=settings.telegram_bot_token, session=session)
    dp = Dispatcher()
    dp.include_router(router)

    await bot.set_my_commands([
        BotCommand(command="token", description="Save your JWT token"),
    ])

    return bot, dp
