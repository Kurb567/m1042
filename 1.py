import asyncio
import signal
from aiogram import Bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = None


async def main() -> None:
    global bot
    bot = Bot(token=BOT_TOKEN)

    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown()))

    while True:
        try:
            user_input = input("Введите user_id (или 'exit' для выхода): ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if user_input.lower() in ("exit", "quit", "q"):
            break
        if not user_input.isdigit():
            print("Введите корректный числовой ID")
            continue

        user_id = int(user_input)

        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Подключить прокси")]],
            resize_keyboard=True
        )

        try:
            await bot.send_message(
                chat_id=user_id,
                text="🚀 Прокси-сервер для Telegram — нажмите для подключения:",
                reply_markup=kb
            )
            print(f"[OK] Сообщение отправлено пользователю {user_id}")
        except Exception as e:
            print(f"[ERROR] {user_id} — {e}")

    await shutdown()


async def shutdown():
    global bot
    if bot:
        await bot.session.close()
        print("\nБот остановлен")


if __name__ == "__main__":
    asyncio.run(main())
