import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from handlers import cmd_start, get_contact_handler
from dialogs import get_phone, get_tier, main_menu
from aiogram_dialog import setup_dialogs

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
dp = Dispatcher()

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=API_TOKEN)
    dp.message.register(cmd_start, CommandStart())
    dp.message.register(get_contact_handler, F.content_type == ContentType.CONTACT)
    dp.include_router(get_phone)
    dp.include_router(get_tier)
    dp.include_router(main_menu)
    setup_dialogs(dp)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())