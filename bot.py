import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! Бот запущен ✅\n"
        "Скоро здесь появится поиск новых объявлений."
    )


async def main():
    if not TOKEN:
        raise RuntimeError("Не задан BOT_TOKEN")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
