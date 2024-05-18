import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, Message, Contact
from aiogram_dialog import DialogManager, setup_dialogs, StartMode
from dialogs import general, GeneralSG
from aiogram.fsm.state import State, StatesGroup
import aiohttp
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
BASE_URL = os.getenv('BASE_URL')
dp = Dispatcher()


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
                await dialog_manager.start(GeneralSG.confirm, mode=StartMode.RESET_STACK, data={'phone_number': phone_number})
            elif resp.status == 200:
                async with session.put(f'{BASE_URL}/users/update/{msg.from_user.id}/', data=user_data) as update_resp:
                    if update_resp.status == 200:
                        await dialog_manager.start(GeneralSG.confirm, mode=StartMode.RESET_STACK, data={'phone_number': phone_number})
            else:
                await msg.reply("Что-то пошло не так. Попробуйте ещё раз.")

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
    dp.include_router(general)
    setup_dialogs(dp)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())