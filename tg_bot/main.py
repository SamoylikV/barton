import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, Message, Contact
from aiogram_dialog import DialogManager, setup_dialogs, StartMode, Window, Dialog
from aiogram.fsm.state import State, StatesGroup
import aiohttp
from dotenv import load_dotenv
from aiogram_dialog.widgets.kbd import Next, Row, Button, Next
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
BASE_URL = os.getenv('BASE_URL')
dp = Dispatcher()

class GetPhoneSG(StatesGroup):
    confirm = State()
    ready = State()
    
class GetInfoSG(StatesGroup):
    choose_tier = State()
    get_name = State()
    get_surname = State()
    get_email = State()
    final = State()
    
async def on_confirm_click(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    if button.widget_id.startswith('choose_tier'):
        dialog_manager.dialog_data['tier'] = button.widget_id
    await dialog_manager.next()
    
async def on_ready_click(callback, button, dialog_manager):
    await dialog_manager.start(GetInfoSG.choose_tier, mode=StartMode.RESET_STACK)

async def send_payment_link(msg: Message, dialog: Dialog, dialog_manager: DialogManager):
    tier = dialog_manager.dialog_data.get('tier')
    if tier == 'choose_tier_1':
        link = "https://example.com/payment/month"
    elif tier == 'choose_tier_2':
        link = "https://example.com/payment/6months"
    elif tier == 'choose_tier_3':
        link = "https://example.com/payment/year"
    else:
        link = "https://example.com/payment/default"
    await dialog_manager.switch_to(GetInfoSG.final)
    await dialog_manager.event.answer(f"Для оплаты перейдите по ссылке: {link}")
    
async def get_name (msg: Message, dialog: Dialog, dialog_manager: DialogManager):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{BASE_URL}/users/update/{msg.from_user.id}/', data={"name": msg.text}) as update_resp:
                if update_resp.status == 200:
                    await dialog_manager.switch_to(GetInfoSG.get_surname)
                    
async def get_surname (msg: Message, dialog: Dialog, dialog_manager: DialogManager):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{BASE_URL}/users/update/{msg.from_user.id}/', data={"surname": msg.text}) as update_resp:
                if update_resp.status == 200:
                    await dialog_manager.switch_to(GetInfoSG.get_email)
                    
async def get_email (msg: Message, dialog: Dialog, dialog_manager: DialogManager):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{BASE_URL}/users/update/{msg.from_user.id}/', data={"email": msg.text}) as update_resp:
                if update_resp.status == 200:
                    await dialog_manager.switch_to(GetInfoSG.final)

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
        state=GetInfoSG.choose_tier
    ),
    Window(
        Const("Ваше имя"),
        MessageInput(get_name),
        state=GetInfoSG.get_name
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

@dp.message(F.content_type == ContentType.CONTACT)
async def get_contact(msg: Message, dialog_manager: DialogManager):
    phone_number = msg.contact.phone_number
    user_data = {
        'tg_id': msg.from_user.id,
        'number': phone_number
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f'{BASE_URL}/users/create/', data=user_data) as resp:
            if resp.status == 201:
                await dialog_manager.start(GetPhoneSG.confirm, mode=StartMode.RESET_STACK, data={'phone_number': phone_number})
            elif resp.status == 200:
                async with session.post(f'{BASE_URL}/users/update/{msg.from_user.id}/', data=user_data) as update_resp:
                    if update_resp.status == 200:
                        await dialog_manager.start(GetPhoneSG.confirm, mode=StartMode.RESET_STACK, data={'phone_number': phone_number})
            else:
                await msg.reply("Что-то пошло не так. Попробуйте ещё раз.")
                

                    
async def send_payment_link(dialog_manager: DialogManager):
    async with dialog_manager.storage.get_data(dialog_manager.event.from_user.id) as data:
        tier = data.get('tier')
        if tier == 'choose_tier_1':
            link = "https://example.com/payment/month"
        elif tier == 'choose_tier_2':
            link = "https://example.com/payment/6months"
        elif tier == 'choose_tier_3':
            link = "https://example.com/payment/year"
        else:
            link = "https://example.com/payment/default"
    await dialog_manager.dialog().switch_to(dialog_manager, GetInfoSG.final)
    await dialog_manager.event.answer(f"Для оплаты перейдите по ссылке: {link}")


async def send_contact(msg: Message):
    markup = ReplyKeyboardMarkup(keyboard=[[
        KeyboardButton(text="Поделиться контактом", request_contact=True)
    ]], resize_keyboard=True, one_time_keyboard=True)
    await msg.reply("Чтобы продолжить пользоваться ботом, вам нужно подтвердить свой номер.", reply_markup=markup)

async def cmd_start(msg: Message, dialog_manager: DialogManager):
    await send_contact(msg)

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=API_TOKEN)
    dp.message.register(cmd_start, CommandStart())
    dp.include_router(get_phone)
    dp.include_router(get_tier)
    setup_dialogs(dp)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

