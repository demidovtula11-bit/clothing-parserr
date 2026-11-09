import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.filters.command import CommandObject

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список брендов каждого пользователя
user_brands = {}


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! 👋\n"
        "Я бот для поиска объявлений об одежде.\n\n"
        "Добавляй любые бренды командой:\n"
        "/addbrand Stone Island\n\n"
        "Напиши /help, чтобы увидеть все команды."
    )


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Команды бота:\n\n"
        "/addbrand название — добавить бренд\n"
        "/removebrand название — удалить бренд\n"
        "/brands — показать твои бренды\n"
        "/clearbrands — очистить список\n"
        "/help — помощь"
    )


@dp.message(Command("addbrand"))
async def add_brand(message: Message, command: CommandObject):
    brand = (command.args or "").strip()

    if not brand:
        await message.answer(
            "Напиши название после команды.\n"
            "Пример: /addbrand Nike"
        )
        return

    brands = user_brands.setdefault(message.from_user.id, [])

    if any(b.casefold() == brand.casefold() for b in brands):
        await message.answer("Этот бренд уже есть в твоём списке.")
        return

    brands.append(brand)
    await message.answer(f"✅ Добавлен бренд: {brand}")


@dp.message(Command("brands"))
async def show_brands(message: Message):
    brands = user_brands.get(message.from_user.id, [])

    if not brands:
        await message.answer(
            "Список пока пуст. Добавь бренд командой /addbrand"
        )
        return

    await message.answer(
        "Твои бренды:\n\n" +
        "\n".join(f"• {brand}" for brand in brands)
    )


@dp.message(Command("removebrand"))
async def remove_brand(message: Message, command: CommandObject):
    brand = (command.args or "").strip()
    brands = user_brands.get(message.from_user.id, [])

    if not brand:
        await message.answer(
            "Пример: /removebrand Nike"
        )
        return

    for existing in brands:
        if existing.casefold() == brand.casefold():
            brands.remove(existing)
            await message.answer(f"Удалён бренд: {existing}")
            return

    await message.answer("Такого бренда нет в твоём списке.")


@dp.message(Command("clearbrands"))
async def clear_brands(message: Message):
    user_brands[message.from_user.id] = []
    await message.answer("Список брендов очищен.")


async def main():
    if not TOKEN:
        raise RuntimeError("Не задан BOT_TOKEN")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
