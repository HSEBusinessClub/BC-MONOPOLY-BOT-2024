from aiogram.fsm.state import StatesGroup, State

class BotState(StatesGroup):
    in_menu_state = State()
    playing_state = State()
    in_progress_with_partner = State()
    in_admin_mode = State()
