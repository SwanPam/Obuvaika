from config import WEB_APP_URL
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards import open_catalog_keyboard
from utils.logger import setup_logger

logger = setup_logger(__name__)

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "👟 Добро пожаловать в обувной магазин!",
        reply_markup=open_catalog_keyboard()
    )

