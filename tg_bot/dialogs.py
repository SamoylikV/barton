from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from datetime import datetime
from asgiref.sync import async_to_sync
import aiohttp
import os

BASE_URL = os.getenv('BASE_URL')

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

async def on_confirm_click(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    if button.widget_id.startswith('choose_tier'):
        dialog_manager.dialog_data['tier'] = button.widget_id
    await dialog_manager.next()
    
async def on_ready_click(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(GetInfoSG.choose_tier, mode=StartMode.RESET_STACK)
    
async def get_label(name: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{BASE_URL}/labels/{name}/') as resp:
            if resp.status == 200:
                label = await resp.json()
                return label.get('text')
                
                
async def send_payment_link(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    tier = dialog_manager.dialog_data.get('tier')
    if tier == 'choose_tier_1':
        link = "https://example.com/payment/month"
    elif tier == 'choose_tier_2':
        link = "https://example.com/payment/6months"
    elif tier == 'choose_tier_3':
        link = "https://example.com/payment/year"
    else:
        link = "https://example.com/payment/default"
    # await dialog_manager.switch_to(GetInfoSG.final)
    # await dialog_manager.event.answer(f"Для оплаты перейдите по ссылке: {link}")
    await dialog_manager.start(MainSG.main, mode=StartMode.RESET_STACK)
    
async def get_name(msg: Message, dialog: Dialog, dialog_manager: DialogManager):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{BASE_URL}/users/update/{msg.from_user.id}/', data={"name": msg.text}) as update_resp:
            if update_resp.status == 200:
                await dialog_manager.switch_to(GetInfoSG.get_surname)
                    
async def get_surname(msg: Message, dialog: Dialog, dialog_manager: DialogManager):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{BASE_URL}/users/update/{msg.from_user.id}/', data={"surname": msg.text}) as update_resp:
            if update_resp.status == 200:
                await dialog_manager.switch_to(GetInfoSG.get_email)
                    
async def get_email(msg: Message, dialog: Dialog, dialog_manager: DialogManager):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{BASE_URL}/users/update/{msg.from_user.id}/', data={"email": msg.text}) as update_resp:
            if update_resp.status == 200:
                await dialog_manager.switch_to(GetInfoSG.final)
                
async def on_platform_click(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    async with aiohttp.ClientSession() as session:
        tg_id = callback.from_user.id
        async with session.get(f'{BASE_URL}/users/{tg_id}') as resp:
            if resp.status == 200:
                user_data = await resp.json()
                if user_data['subscription_expiration'] is not None and user_data['subscription_expiration'] > datetime.now():
                    await dialog_manager.switch_to(MainSG.platform)
                else:
                    await dialog_manager.switch_to(MainSG.declined)
                    
async def on_back_click(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(MainSG.main)
    

get_phone = Dialog(
    Window(
        Format("Твой номер: {start_data[phone_number]}?"),
        Button(Const(async_to_sync(get_label)('next')), id='confirm', on_click=on_ready_click),
        state=GetPhoneSG.confirm
    ),
    Window(Const(async_to_sync(get_label)('all_done')), state=GetPhoneSG.ready)
)

get_tier = Dialog(
    Window(
        Const(async_to_sync(get_label)('choose_tier')),
        Button(Const(async_to_sync(get_label)('tier_1')), id='choose_tier_1', on_click=on_confirm_click),
        Button(Const(async_to_sync(get_label)('tier_2')), id='choose_tier_2', on_click=on_confirm_click),
        Button(Const(async_to_sync(get_label)('tier_3')), id='choose_tier_3', on_click=on_confirm_click),
        state=GetInfoSG.choose_tier,
    ),
    Window(
        Const(async_to_sync(get_label)('name')),
        MessageInput(get_name),
        state=GetInfoSG.get_name,
    ),
    Window(
        Const(async_to_sync(get_label)('surname')),
        MessageInput(get_surname),
        state=GetInfoSG.get_surname
    ),
    Window(
        Const(async_to_sync(get_label)('email')),
        MessageInput(get_email),
        state=GetInfoSG.get_email
    ),
    Window(
        Const(async_to_sync(get_label)('thanks')),
        Button(Const(async_to_sync(get_label)('get_link')), id='get_payment_link', on_click=send_payment_link),
        state=GetInfoSG.final
    )
)

main_menu = Dialog(
    Window(
        Const(async_to_sync(get_label)('menu')),
        Button(Const(async_to_sync(get_label)('platform')), id='platform', on_click=on_platform_click),
        Button(Const(async_to_sync(get_label)('library')), id='library'),
        Button(Const(async_to_sync(get_label)('free_help')), id='free_help'),
        Button(Const(async_to_sync(get_label)('club_discount')), id='club_discount'),
        Button(Const(async_to_sync(get_label)('neuro_mark')), id='neuro_mark'),
        Button(Const(async_to_sync(get_label)('nearest_events')), id='nearest_events'),
        markup_factory=ReplyKeyboardFactory(resize_keyboard=True, one_time_keyboard=False),
        state=MainSG.main
    ),
    Window(
        Const(async_to_sync(get_label)('platform')),
        Button(Const(async_to_sync(get_label)('back')), id='back', on_click=on_back_click),
        state=MainSG.platform
    ),
    Window(
        Const(async_to_sync(get_label)('declined')),
        Button(Const(async_to_sync(get_label)('back')), id='back', on_click=on_back_click),
        state=MainSG.declined
    )
)