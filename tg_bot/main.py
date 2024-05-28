import os
import sys
import logging
import asyncio
import django
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from handlers import cmd_start, get_contact_handler
from dialogs import get_phone, get_tier, main_menu
from aiogram_dialog import setup_dialogs
from handlers import initialize_labels_cache, check_subscriptions
from asgiref.sync import sync_to_async
from apscheduler.schedulers.asyncio import AsyncIOScheduler


load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../backend")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

API_TOKEN = os.getenv('API_TOKEN')
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

async def initialize_cache_if_needed():
    from api.signals import update_label_cache, get_cache_file_path
    cache_file_path = get_cache_file_path()
    if not os.path.exists(cache_file_path):
        await sync_to_async(update_label_cache)()
        
def schedule_jobs():
    scheduler.add_job(check_subscriptions, 'cron', hour=0)


async def main():
    logging.basicConfig(level=logging.INFO)
    dp.message.register(cmd_start, CommandStart())
    dp.message.register(get_contact_handler, F.content_type == ContentType.CONTACT)
    dp.include_router(get_phone)
    dp.include_router(get_tier)
    dp.include_router(main_menu)
    setup_dialogs(dp)
    await initialize_cache_if_needed()
    await initialize_labels_cache()
    schedule_jobs()
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())