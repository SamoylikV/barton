from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
import aiohttp
import os
from dialogs import GetPhoneSG, MainSG, get_label
from datetime import datetime


BASE_URL = os.getenv('BASE_URL')

async def cmd_start(msg: Message, dialog_manager: DialogManager):
    await send_contact(msg)

async def send_contact(msg: Message):
    markup = ReplyKeyboardMarkup(keyboard=[[
        KeyboardButton(text="Поделиться контактом", request_contact=True)
    ]], resize_keyboard=True, one_time_keyboard=True)
    # await msg.reply("Чтобы продолжить пользоваться ботом, вам нужно подтвердить свой номер.", reply_markup=markup)
    await msg.reply(await get_label('give_number'), reply_markup=markup)

async def get_contact_handler(msg: Message, dialog_manager: DialogManager):
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
                await msg.reply(await get_label('error'))
                # await msg.reply("Что-то пошло не так. Попробуйте ещё раз.")
                
