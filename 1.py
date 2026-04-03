import asyncio
from aiogram import Bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"


async def main() -> None:
    bot = Bot(token=BOT_TOKEN)

    while True:
        user_input = input("Введите user_id (или 'exit' для выхода): ").strip()
        if user_input.lower() in ("exit", "quit", "q"):
            break
        if not user_input.isdigit():
            print("Введите корректный числовой ID")
            continue

        user_id = int(user_input)

        # Создаём клавиатуру с кнопкой
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

    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
