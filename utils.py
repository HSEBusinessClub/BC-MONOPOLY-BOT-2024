import random

from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types as aiogram_types

async def generate_partners_buttons(state: FSMContext):
    user_data = await state.get_data()
    print(user_data)
    keyboard_builder = ReplyKeyboardBuilder()
    num_partners_to_visit = 0

    for partner_name in user_data:
        if not user_data[partner_name]:
            num_partners_to_visit += 1
            keyboard_builder.add(aiogram_types.KeyboardButton(text=partner_name))

    keyboard_builder.adjust(2)
    
    keyboard = keyboard_builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Смелее!"
    )

    return keyboard

def generate_motivating_phrase():
    l = ["Не останавливайся на достигнутом!", "Продолжай двигаться вперёд, несмотря ни на что!",
         "Каждый шаг приближает тебя к цели!", "Верь в себя и продолжай идти!",
         "Возможности есть всегда, продолжай искать их!", "Ты можешь больше, чем думаешь!",
         "Твоя жизнь — в твоих руках, продолжай строить её!", "Успех требует усилий, продолжай работать над собой!",
         "Ты можешь всё, продолжай верить в себя!" ]
    return l[random.randint(0, len(l)-1)]
