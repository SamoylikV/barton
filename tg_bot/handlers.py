from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, ChatMemberAdministrator
from aiogram_dialog import DialogManager, StartMode, Dialog
from aiogram_dialog.widgets.kbd import Button
from aiogram import Bot
import aiohttp
import asyncio
import os
import sys
from states import GetPhoneSG, GetInfoSG, MainSG
from datetime import datetime
import json
from django.utils import timezone
from django.db.models import Q
from asgiref.sync import sync_to_async

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../backend")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

BASE_URL = os.getenv('BASE_URL')
CACHE_FILE = 'label_cache.json'
labels_cache = None

async def load_labels_from_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as cache_file:
            return json.load(cache_file)
    return {}

async def initialize_labels_cache():
    global labels_cache
    labels_cache = await load_labels_from_cache()

async def get_label(name: str):
    if labels_cache is None:
        await initialize_labels_cache()
    return labels_cache.get(name)

async def cmd_start(msg: Message, dialog_manager: DialogManager):
    from api.models import Groups
    if msg.chat.type == 'private':
        await send_contact(msg)
    else:
        chat_id = str(msg.chat.id)
        group, created = await sync_to_async(Groups.objects.get_or_create, thread_sensitive=True)(chat_id=chat_id)
        await check_subscriptions()

async def send_contact(msg: Message):
    if msg.chat.type == 'private':
        markup = ReplyKeyboardMarkup(keyboard=[[
            KeyboardButton(text="Поделиться контактом", request_contact=True)
        ]], resize_keyboard=True, one_time_keyboard=True)
        # await msg.reply("Чтобы продолжить пользоваться ботом, вам нужно подтвердить свой номер.", reply_markup=markup)
        await msg.reply(await get_label('give_number'), reply_markup=markup)
    else:
        await msg.reply("123")

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
    

async def get_group_chat_ids():
    from api.models import Groups
    groups = await sync_to_async(list)(Groups.objects.all())
    return [group.chat_id for group in groups]    

    
async def get_expired_users():
    from api.models import User
    query = Q(subscription_expiration__lt=timezone.now()) | Q(subscription_expiration__isnull=True)
    users = await sync_to_async(list)(User.objects.filter(query).values_list('tg_id', flat=True))
    return users

async def check_subscriptions():
    from main import bot
    group_chat_ids = await get_group_chat_ids()
    for chat_id in group_chat_ids:
        admin_list = [admin.user.id for admin in await bot.get_chat_administrators(chat_id)]
        users = await get_expired_users()
        for user in users:
            try:
                if user not in admin_list:
                    await bot.ban_chat_member(chat_id=chat_id, user_id=user)
            except Exception as e:
                print(e)

            
            