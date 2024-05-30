import os
import asyncio
import time

from aiogram.types import FSInputFile
from aiogram import Bot, Dispatcher, types as aiogram_types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from aiogram.enums import ParseMode
from aiogram import F

from db import init_db, ADD_USER, ADD_NOTE, GET_ALL_USERS as GET_ALL_CHAT_ID
from state import BotState
from text.greeting_text import TEXT as HTML_GREETING_TEXT
from text.start_game_text import TEXT as HTML_START_GAME_TEXT
from utils import generate_motivating_phrase, generate_partners_buttons
from text.partners_desc.partners_dict import PARTNERS_DESCRIPTION

load_dotenv(override=True)

MONOPOLY_TEXT = "Монополия"
START_GAME_TEXT = "Поехали!"
SUCCESS_TEXT = "Успех!"
BACK_TO_PARTNERS_TEXT = "К партнёрам"
PROGRAM_LIST = "Программа форума"
IN_PROGRESS = "In Progress"
PARTNERS = PARTNERS_DESCRIPTION.keys()
SECRET_CODE = os.environ["SECRET_ADMIN_CODE"]


base_user_data = dict(zip(PARTNERS, [False] * len(PARTNERS)))

bc_bot = Bot(token=os.getenv("TELEGRAM_API_TOKEN"))
dp = Dispatcher()
con, cur = init_db()

@dp.message(Command("start"))
async def start_cmd(message: aiogram_types.Message, state: FSMContext):

    kb = [[aiogram_types.KeyboardButton(text=START_GAME_TEXT)]]
    keyboard = aiogram_types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="форум ждёт!!"
    )

    await state.set_state(BotState.in_menu_state)
    await state.set_data(base_user_data)
    await message.answer(
        HTML_GREETING_TEXT,
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )


@dp.message(Command("timeline"))
async def send_program(message: aiogram_types.Message):
    image_from_pc = FSInputFile("./text/HSE_Business_Club_2024.pdf")

    kb = [[aiogram_types.KeyboardButton(text=START_GAME_TEXT)]]
    keyboard = aiogram_types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="форум ждёт!!"
    )

    await message.answer_document(
        image_from_pc,
        caption="Программа форума",
        reply_markup=keyboard
    )


@dp.message(F.text == SECRET_CODE)
async def secret_cmd(message: aiogram_types.Message, state: FSMContext):
    await state.set_state(BotState.in_admin_mode)
    await message.answer("Введите текст для рассылки следующим сообщением!")


@dp.message(BotState.in_admin_mode)
async def send_message(message: aiogram_types.Message, state: FSMContext):
    cur.execute(GET_ALL_CHAT_ID())
    chats_id = cur.fetchall()
    payload_timer = 0

    for current_chat_id in chats_id:
        payload_timer += 1

        try:
            await bc_bot.copy_message(int(current_chat_id[0]), message.chat.id, message.message_id)
        except Exception as e:
            print(e)

        if payload_timer % 20 == 0:
            time.sleep(3)

    await state.set_state(BotState.in_menu_state)
    await message.answer("Рассылка проведена успешно")


@dp.message(F.text == START_GAME_TEXT)
async def start_game(message: aiogram_types.Message, state: FSMContext):

    await state.set_state(BotState.playing_state)
    partners_keyboard = await generate_partners_buttons(state)

    add_person_query = ADD_USER(message.chat.id)
    cur.execute(add_person_query)
    con.commit()
    print("player added")

    await message.answer(
        HTML_START_GAME_TEXT,
        parse_mode=ParseMode.HTML,
        reply_markup=partners_keyboard
    )


@dp.message(
    BotState.playing_state,
    F.text.in_(PARTNERS)
)
async def choose_partner(message: aiogram_types.Message, state: FSMContext):

    user_data = await state.get_data()
    user_data[message.text] = IN_PROGRESS
    await state.set_data(user_data)
    await state.set_state(BotState.in_progress_with_partner)
    partner_html_desc = PARTNERS_DESCRIPTION[message.text]

    kb = [[aiogram_types.KeyboardButton(text=SUCCESS_TEXT), aiogram_types.KeyboardButton(text=BACK_TO_PARTNERS_TEXT)]]
    keyboard = aiogram_types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )

    await message.answer(
        partner_html_desc,
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )


@dp.message(
    BotState.in_progress_with_partner,
    F.text.in_([SUCCESS_TEXT, BACK_TO_PARTNERS_TEXT])
)
async def to_partners(message: aiogram_types.Message, state: FSMContext):
    user_data = await state.get_data()
    are_all_done = True

    for partner in user_data:
        if user_data[partner] == IN_PROGRESS:
            if message.text == SUCCESS_TEXT:
                user_data[partner] = True

                add_success_note_query = ADD_NOTE(message.chat.id, partner)
                cur.execute(add_success_note_query)
                con.commit()
                print("note added")
            else:
                user_data[partner] = False
        if user_data[partner] == False:
            are_all_done = False
    
    await state.set_state(BotState.playing_state)
    await state.set_data(user_data)


    partners_keyboard = await generate_partners_buttons(state)
    ans_text = None
    if are_all_done:
        ans_text = "Молодец!! \nПодарки заберешь позже"
    elif message.text == SUCCESS_TEXT:
        ans_text = generate_motivating_phrase()
    else:
        ans_text = "Можешь продолжить позже!"

    await message.answer(
        ans_text,
        parse_mode=ParseMode.HTML,
        reply_markup=partners_keyboard
    )


async def main():
    await dp.start_polling(bc_bot)


if __name__ == "__main__":
    asyncio.run(main())
