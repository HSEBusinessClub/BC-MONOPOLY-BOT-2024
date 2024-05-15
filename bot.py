import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv
from aiogram.enums import ParseMode
from aiogram import F

from text.greeting_text import TEXT as HTML_GREETING_TEXT

load_dotenv()

MONOPOLY = "Монополия"

bc_bot = Bot(token=os.getenv("TELEGRAM_API_TOKEN"))
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):

    kb = [[types.KeyboardButton(text=MONOPOLY)]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)

    await message.answer(
        "starting...",
        reply_markup=keyboard
    )

@dp.message(F.text == MONOPOLY)
async def run_desc(message: types.Message):
    await message.answer(
        HTML_GREETING_TEXT,
        parse_mode=ParseMode.HTML
    )

async def main():
    await dp.start_polling(bc_bot)


if __name__ == "__main__":
    asyncio.run(main())