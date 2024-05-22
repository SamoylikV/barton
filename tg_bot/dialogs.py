from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import aiohttp
import os
from datetime import datetime

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
        Format("Ваш номер: {start_data[phone_number]}"),
        Button(Const("Дальше"), id='confirm', on_click=on_ready_click),
        state=GetPhoneSG.confirm
    ),
    Window(Const("Все готово"), state=GetPhoneSG.ready)
)

get_tier = Dialog(
    Window(
        Const("Выберите тариф"),
        Button(Const("На месяц"), id='choose_tier_1', on_click=on_confirm_click),
        Button(Const("На 6 месяцев"), id='choose_tier_2', on_click=on_confirm_click),
        Button(Const("На год"), id='choose_tier_3', on_click=on_confirm_click),
        state=GetInfoSG.choose_tier,
    ),
    Window(
        Const("Ваше имя"),
        MessageInput(get_name),
        state=GetInfoSG.get_name,
    ),
    Window(
        Const("Ваша фамилия"),
        MessageInput(get_surname),
        state=GetInfoSG.get_surname
    ),
    Window(
        Const("Ваш email"),
        MessageInput(get_email),
        state=GetInfoSG.get_email
    ),
    Window(
        Const("Спасибо за предоставленные данные!"),
        Button(Const("Получить ссылку для оплаты"), id='get_payment_link', on_click=send_payment_link),
        state=GetInfoSG.final
    )
)

main_menu = Dialog(
    Window(
        Const("Меню"),
        Button(Const("Платформа"), id='platform', on_click=on_platform_click),
        Button(Const("Библиотека знаний"), id='library'),
        Button(Const("Бесплатная помощь"), id='free_help'),
        Button(Const("Клубные скидки"), id='club_discount'),
        Button(Const("Нейромарк"), id='neuro_mark'),
        Button(Const("Ближайшие мероприятия"), id='nearest_events'),
        markup_factory=ReplyKeyboardFactory(resize_keyboard=True, one_time_keyboard=False),
        state=MainSG.main
    ),
    Window(
        Const("Платформа"),
        Button(Const("Назад"), id='back', on_click=on_back_click),
        state=MainSG.platform
    ),
    Window(
        Const("У вас нет доступа"),
        Button(Const("Назад"), id='back', on_click=on_back_click),
        state=MainSG.declined
    )
)