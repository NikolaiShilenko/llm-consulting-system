from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.bot.dispatcher import setup_bot
    from aiogram.types import Update

    bot, dp = await setup_bot()
    asyncio.create_task(dp.start_polling(bot))

    yield

    await bot.session.close()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    @app.get("/health")
    async def health():
        return {"status": "ok", "env": settings.env}

    return app


app = create_app()
