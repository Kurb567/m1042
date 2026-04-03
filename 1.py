import asyncio
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
USERS_FILE = "1.txt"
MESSAGE = "🚀 Прокси-сервер для Telegram — нажмите для подключения:"


def read_user_ids(filepath: str) -> list[int]:
    """Читает ID пользователей из файла (по одному на строку)."""
    user_ids = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    user_ids.append(int(line))
                except ValueError:
                    pass
    return user_ids


async def send_to_user(bot: Bot, user_id: int, text: str) -> bool:
    """Отправляет сообщение пользователю. Возвращает True при успехе."""
    try:
        await bot.send_message(chat_id=user_id, text=text)
        print(f"[OK] {user_id}")
        return True
    except TelegramRetryAfter as e:
        print(f"[RATE LIMIT] {user_id} — ждём {e.retry_after}с")
        await asyncio.sleep(e.retry_after)
        return await send_to_user(bot, user_id, text)
    except TelegramForbiddenError:
        print(f"[BLOCKED] {user_id}")
        return False
    except Exception as e:
        print(f"[ERROR] {user_id} — {e}")
        return False


async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    user_ids = read_user_ids(USERS_FILE)
    print(f"Найдено пользователей: {len(user_ids)}")

    success = 0
    for uid in user_ids:
        if await send_to_user(bot, uid, MESSAGE):
            success += 1
        await asyncio.sleep(0.05)

    print(f"\nОтправлено: {success}/{len(user_ids)}")
    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
