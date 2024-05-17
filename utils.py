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
