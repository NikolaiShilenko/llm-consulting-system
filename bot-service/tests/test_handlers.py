import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import fakeredis.aioredis


@pytest.mark.asyncio
async def test_save_token():
    fake_redis = fakeredis.aioredis.FakeRedis()

    with patch("app.bot.handlers.get_redis", return_value=fake_redis):
        with patch("app.bot.handlers.decode_and_validate") as mock_decode:
            mock_decode.return_value = {"sub": "1", "role": "user"}

            message = MagicMock()
            message.text = "/token test.jwt.token"
            message.from_user = MagicMock()
            message.from_user.id = 12345
            message.answer = AsyncMock()

            from app.bot.handlers import save_token
            await save_token(message)

            # Декодируем bytes в строку
            saved_token = await fake_redis.get("tg_user:12345:jwt")
            assert saved_token.decode() == "test.jwt.token"
            message.answer.assert_called_once()


@pytest.mark.asyncio
async def test_handle_message_without_token():
    fake_redis = fakeredis.aioredis.FakeRedis()

    with patch("app.bot.handlers.get_redis", return_value=fake_redis):
        message = MagicMock()
        message.text = "Hello"
        message.from_user = MagicMock()
        message.from_user.id = 12345
        message.answer = AsyncMock()

        from app.bot.handlers import handle_message
        await handle_message(message)

        message.answer.assert_called_once_with(
            "No token found. Please register at Auth Service and use /token <jwt>"
        )


@pytest.mark.asyncio
async def test_handle_message_with_valid_token():
    fake_redis = fakeredis.aioredis.FakeRedis()
    await fake_redis.set("tg_user:12345:jwt", "valid.jwt.token")

    with patch("app.bot.handlers.get_redis", return_value=fake_redis):
        with patch("app.bot.handlers.decode_and_validate") as mock_decode:
            mock_decode.return_value = {"sub": "1", "role": "user"}

            with patch("app.bot.handlers.llm_request") as mock_llm_request:
                mock_task = MagicMock()
                mock_task.get.return_value = "Test response from LLM"
                mock_llm_request.delay.return_value = mock_task

                message = MagicMock()
                message.text = "Hello"
                message.from_user = MagicMock()
                message.from_user.id = 12345
                message.answer = AsyncMock()

                from app.bot.handlers import handle_message
                await handle_message(message)

                assert message.answer.call_count >= 2


@pytest.mark.asyncio
async def test_handle_message_with_expired_token():
    fake_redis = fakeredis.aioredis.FakeRedis()
    await fake_redis.set("tg_user:12345:jwt", "expired.jwt.token")

    with patch("app.bot.handlers.get_redis", return_value=fake_redis):
        with patch("app.bot.handlers.decode_and_validate") as mock_decode:
            mock_decode.side_effect = ValueError("Token expired")

            message = MagicMock()
            message.text = "Hello"
            message.from_user = MagicMock()
            message.from_user.id = 12345
            message.answer = AsyncMock()

            from app.bot.handlers import handle_message
            await handle_message(message)

            message.answer.assert_called_once_with("Token expired or invalid: Token expired")
