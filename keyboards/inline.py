from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import WebAppInfo
from config import WEB_APP_URL


def open_catalog_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Открыть каталог",
                                                                       web_app=WebAppInfo(url=WEB_APP_URL)
            )]
        ])