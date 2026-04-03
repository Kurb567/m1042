import asyncio
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter

BOT_TOKEN = "8557116313:AAEqp_YBnxLfXZX9VVP5Dtg5XtRZFvIySgw"
MESSAGE = "🚀 Прокси-сервер для Telegram — нажмите для подключения:\n\n https://t.me/proxy?server=tg.capycore.ru&port=443&secret=27ebe852539fb8ec5f327c73262bb721"
USERS_FILE = "1.txt"


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


async def send_to_user(bot, user_id, text):
    """Отправляет сообщение пользователю. Возвращает True при успехе."""
    try:
        await bot.send_message(chat_id=user_id, text=text)
        print(f"[OK] Сообщение отправлено: {user_id}")
        return True
    except TelegramRetryAfter as e:
        print(f"[RATE LIMIT] {user_id} — ждём {e.retry_after}с")
        await asyncio.sleep(e.retry_after)
        return await send_to_user(bot, user_id, text)
    except TelegramForbiddenError:
        print(f"[BLOCKED] {user_id} — бот заблокирован")
        return False
    except Exception as e:
        print(f"[ERROR] {user_id} — {e}")
        return False


async def broadcast(user_ids: list[int], text: str):
    """Рассылает сообщение всем пользователям из списка."""
    bot = Bot(token=BOT_TOKEN)
    success = 0
    failed = 0

    for uid in user_ids:
        if await send_to_user(bot, uid, text):
            success += 1
        else:
            failed += 1  # небольшая задержка между отправками

    print(f"\nРассылка завершена!")
    print(f"Успешно: {success}")
    print(f"Не удалось: {failed}")
    await bot.session.close()


async def main() -> None:
    user_ids = read_user_ids(USERS_FILE)
    print(f"Найдено пользователей: {len(user_ids)}")
    await broadcast(user_ids, MESSAGE)


if __name__ == "__main__":
    asyncio.run(main())
