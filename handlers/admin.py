from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from lexicon.lexicon_ru import LEXICON


admin_router = Router()


@admin_router.message(Command(commands=['admin']))
async def command_admin(message: Message):
    await message.answer(text=f'{LEXICON["admin"]}, {message.from_user.first_name}')