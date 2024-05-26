from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from asgiref.sync import async_to_sync
import os
from handlers import on_confirm_click, on_ready_click, get_label, get_name, get_surname, get_email, on_platform_click, send_payment_link, on_back_click
from states import GetPhoneSG, GetInfoSG, MainSG

BASE_URL = os.getenv('BASE_URL')             


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