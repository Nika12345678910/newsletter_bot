from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon_ru import LEXICON, btns, format_profile
from FSM.fsm import UserDataFSM
from database.query_orm import (add_user_orm,
                                get_user_orm,
                                get_rooms_orm,
                                get_room_orm)
from keyboard.inline import get_callback_btns
from filter.filter import NameFilter


user_router = Router()


@user_router.message(CommandStart())
async def command_start(message: Message, session: AsyncSession):
    await message.answer(f'{LEXICON["start"]}, {message.from_user.first_name}')
    if await get_user_orm(session, int(message.from_user.id)):
        await message.answer(text=LEXICON["possibilities_user"],
                             reply_markup=get_callback_btns(btns=btns["possibilities_user"]))
        return
    await message.answer(text=LEXICON["registration"],
                         reply_markup=get_callback_btns(btns=btns["registation"]))


#Registration user
@user_router.callback_query(F.data == "registration")
async def start_registration(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON["first_name"])
    await state.set_state(UserDataFSM.first_name)
    await callback.answer()


@user_router.message(NameFilter(), UserDataFSM.first_name)
async def add_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer(text=LEXICON["last_name"])
    await state.set_state(UserDataFSM.last_name)


@user_router.message(NameFilter(), UserDataFSM.last_name)
async def add_last_name(message: Message, state: FSMContext, session: AsyncSession):
    rooms = await get_rooms_orm(session)
    btns = {room.number: str(room.id) for room in rooms}
    await state.update_data(last_name=message.text)
    await message.answer(text=LEXICON["room"], reply_markup=get_callback_btns(btns=btns))
    await state.set_state(UserDataFSM.id_room)


@user_router.callback_query(UserDataFSM.id_room)
async def add_room(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    await state.update_data(id_room=int(callback.data))

    data = await state.get_data()
    data["id_chat"]=callback.from_user.id

    try:
        await add_user_orm(session, data)
        await callback.answer(text=LEXICON["registration_close"])
        await callback.message.answer(text=LEXICON["possibilities_user"],
                             reply_markup=get_callback_btns(btns=btns["possibilities_user"]))
        await state.clear()
    except Exception as e:
        await callback.message.answer(
            f"Ошибка: \n{str(e)}\nЧто-то пошло не так при добавлении данных пользователя в БД",
            reply_markup=get_callback_btns(btns=btns["registation"]),
        )
        await callback.answer()
        await state.clear()


@user_router.message(UserDataFSM.first_name)
async def add_first_name2(messagge: Message, state: FSMContext):
    await messagge.answer(text=LEXICON["error_first_name"])


@user_router.message(UserDataFSM.last_name)
async def add_last_name2(messagge: Message, state: FSMContext):
    await messagge.answer(text=LEXICON["error_last_name"])


@user_router.message(UserDataFSM.id_room)
async def add_room2(messagge: Message, state: FSMContext):
    await messagge.answer(text=LEXICON["error_room"])


#Просмотр профиля
@user_router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery, session: AsyncSession):
    user_data = await get_user_orm(session, int(callback.from_user.id))
    room = await get_room_orm(session, int(user_data.id_room))
    profile = format_profile(user_data.first_name, user_data.last_name, room.number)
    await callback.message.answer(text=profile)


'''#Просмотр расписания
@user_router.callback_query(F.data == "view schedule")
async def view_schedule(callback: CallbackQuery, session: AsyncSession):'''