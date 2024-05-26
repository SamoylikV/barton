from aiogram.fsm.state import State, StatesGroup


class GetPhoneSG(StatesGroup):
    confirm = State()
    ready = State()
    
class GetInfoSG(StatesGroup):
    choose_tier = State()
    get_name = State()
    get_surname = State()
    get_email = State()
    final = State()

class MainSG(StatesGroup):
    main = State()
    platform = State()
    declined = State()