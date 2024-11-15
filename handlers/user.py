from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from lexicon.lexicon_ru import LEXICON


user_router = Router()


@user_router.message(CommandStart())
async def command_start(message: Message):
    await message.answer(f'{LEXICON["start"]}, {message.from_user.first_name}')