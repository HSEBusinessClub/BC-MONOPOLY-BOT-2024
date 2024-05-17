import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, types as aiogram_types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from aiogram.enums import ParseMode
from aiogram import F

from state import BotState
from text.greeting_text import TEXT as HTML_GREETING_TEXT
from text.start_game_text import TEXT as HTML_START_GAME_TEXT
from utils import generate_partners_buttons

load_dotenv(override=True)

MONOPOLY_TEXT = "Монополия"
START_GAME_TEXT = "Поехали!"
partners = ["Level group", "BC questions", "Технологии доверия", "BC photobooth", \
            "hse inc", "BC networking", "Малый бизнес Москвы", "Альфа банк", "SuperJob", \
            "ТеДо", "Beyond Taylor", "Kept", "Фонд содействия инновациям", "аэропорт \"Домодедово\"", \
            "Сибур", "ВТБ"]

base_user_data = dict(zip(partners, [False] * len(partners)))

print(os.getenv("TELEGRAM_API_TOKEN"))
bc_bot = Bot(token=os.getenv("TELEGRAM_API_TOKEN"))
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: aiogram_types.Message, state: FSMContext):

    kb = [[aiogram_types.KeyboardButton(text=MONOPOLY_TEXT)]]
    keyboard = aiogram_types.ReplyKeyboardMarkup(keyboard=kb)

    await message.answer(
        "starting...",
        reply_markup=keyboard
    )
    await state.set_state(BotState.in_menu_state)
    await state.set_data(base_user_data)

@dp.message(F.text == MONOPOLY_TEXT)
async def run_desc(message: aiogram_types.Message):

    kb = [[aiogram_types.KeyboardButton(text=START_GAME_TEXT)]]
    keyboard = aiogram_types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="форум ждёт!!"
    )

    await message.answer(
        HTML_GREETING_TEXT,
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@dp.message(F.text == START_GAME_TEXT)
async def start_game(message: aiogram_types.Message, state: FSMContext):

    await state.set_state(BotState.playing_state)
    partners_keyboard = await generate_partners_buttons(state)

    await message.answer(
        HTML_START_GAME_TEXT,
        parse_mode=ParseMode.HTML,
        reply_markup=partners_keyboard
    )


async def main():
    await dp.start_polling(bc_bot)


if __name__ == "__main__":
    asyncio.run(main())