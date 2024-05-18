from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, DialogManager, setup_dialogs, StartMode, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Next, Row, Button, Next
from aiogram_dialog.widgets.text import Const, Format

class GeneralSG(StatesGroup):
    confirm = State()
    ready = State()
    
async def on_confirm_click(callback, button, manager: DialogManager):
    await manager.next()


general = Dialog(
    Window(
        Format("Ваш номер: {start_data[phone_number]}"),
        Button(Const("Дальше"), id='confirm', on_click=on_confirm_click),
        state=GeneralSG.confirm
    ),
    Window(Const("Все готово"), state=GeneralSG.ready)
)
