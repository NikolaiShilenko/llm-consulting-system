import asyncio
from aiogram import Router, types
from aiogram.filters import Command
from app.infra.redis import get_redis
from app.core.jwt import decode_and_validate
from app.tasks.llm_tasks import llm_request

router = Router()


@router.message(Command("token"))
async def save_token(message: types.Message):
    token = message.text.replace("/token", "").strip()
    if not token:
        await message.answer("Usage: /token <your_jwt_token>")
        return

    try:
        payload = decode_and_validate(token)
        user_id = payload.get("sub")
        if not user_id:
            await message.answer("Invalid token: missing sub")
            return
    except ValueError as e:
        await message.answer(f"Invalid token: {str(e)}")
        return

    redis = await get_redis()
    await redis.set(f"tg_user:{message.from_user.id}:jwt", token)

    await message.answer(f"Token saved for user_id={user_id}")


@router.message()
async def handle_message(message: types.Message):
    redis = await get_redis()
    token = await redis.get(f"tg_user:{message.from_user.id}:jwt")

    if not token:
        await message.answer(
            "No token found. Please register at Auth Service and use /token <jwt>"
        )
        return

    try:
        payload = decode_and_validate(token)
        user_id = payload.get("sub")
    except ValueError as e:
        await message.answer(f"Token expired or invalid: {str(e)}")
        return

    await message.answer("Processing your request...")

    task = llm_request.delay(message.text, int(user_id))
    try:
        result = task.get(timeout=60)
        await message.answer(result)
    except Exception as e:
        await message.answer(f"Error: {str(e)}")
