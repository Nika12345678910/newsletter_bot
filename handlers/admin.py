from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from sqlalchemy.ext.asyncio import AsyncSession

from datetime import time, date

from lexicon.lexicon_ru import LEXICON, btns, format_schedule, check_schedule_kb
from keyboard.reply import create_keyboard
from keyboard.inline import get_callback_btns
from FSM.fsm import AddScheduleFSM
from filter.filter import DateFilter, TimeFilter
from database.query_orm import (get_rooms_orm,
                                add_schedule_orm,
                                get_room_orm,
                                get_id_chats_orm)


admin_router = Router()

admin_kb = create_keyboard(btns["possibilities_admin"],
                           placeholder=btns["placeholder_admin_kb"])


@admin_router.message(Command(commands=['admin']))
async def command_admin(message: Message):
    await message.answer(text=f'{LEXICON["admin"]}, {message.from_user.first_name}',
                         reply_markup=admin_kb)


@admin_router.message(F.text == "Создание расписания", StateFilter(default_state))
async def create_schedule(message: Message, state: FSMContext):
    await message.answer(text=LEXICON["date"],
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddScheduleFSM.date)


@admin_router.message(DateFilter(), AddScheduleFSM.date)
async def add_date(message: Message, state: FSMContext):
    soo = message.text.split('/')
    var_date = date(int(soo[0]), int(soo[1]), int(soo[2]))

    await state.update_data(date=var_date)
    await message.answer(text=LEXICON["time"])
    await state.set_state(AddScheduleFSM.time)


@admin_router.message(TimeFilter(), AddScheduleFSM.time)
async def add_time(message: Message, state: FSMContext, session: AsyncSession):
    rooms = await get_rooms_orm(session)
    btns = {room.number: str(room.id) for room in rooms}

    soo = message.text.split(':')
    var_time = time(int(soo[0]), int(soo[1]), 0)

    await state.update_data(time=var_time)
    await message.answer(text=LEXICON["room"],
                         reply_markup=get_callback_btns(btns=btns))
    await state.set_state(AddScheduleFSM.id_room)


@admin_router.callback_query(AddScheduleFSM.id_room)
async def add_room(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    await state.update_data(id_room=int(callback.data))

    data = await state.get_data()
    room = await get_room_orm(session, int(callback.data))
    schedule = format_schedule(data["date"], data["time"], room.number)

    btns = check_schedule_kb(data)

    await callback.message.answer(text=f'{LEXICON["check_schedule"]}\n{schedule}',
                                  reply_markup=get_callback_btns(btns=btns))
    await state.clear()


@admin_router.message(AddScheduleFSM.date)
async def add_date2(message: Message):
    await message.answer(text=LEXICON["error_date"])


@admin_router.message(AddScheduleFSM.time)
async def add_time2(message: Message):
    await message.answer(text=LEXICON["error_time"])


@admin_router.message(AddScheduleFSM.id_room)
async def add_room2(message: Message):
    await message.answer(text=LEXICON["error_room"])


@admin_router.callback_query(F.data.startswith("confirm_"))
async def public_schedule(callback: CallbackQuery, session: AsyncSession, bot: Bot):
    data = callback.data.split('_')

    soo = data[1].split('-')
    var_date = date(int(soo[0]), int(soo[1]), int(soo[2]))

    soo = data[2].split(':')
    var_time = time(int(soo[0]), int(soo[1]), 0)

    data = {"date": var_date,
            "time": var_time,
            "id_room": int(data[3])}

    room = await get_room_orm(session, data["id_room"])
    schedule = format_schedule(data["date"], data["time"], room.number)

    try:
        await add_schedule_orm(session, data)
        id_chats = await get_id_chats_orm(session)
        for id_chat in id_chats:
            await bot.send_message(id_chat,
                                text=schedule)
        await callback.message.answer(text=f'{LEXICON["public_schedule"]}',
                                  reply_markup=admin_kb)
        await callback.answer()
    except Exception as e:
        await callback.message.answer(
            f"Ошибка: \n{str(e)}\nЧто-то пошло не так при добавлении расписания в БД",
            reply_markup=admin_kb)
        await callback.answer()
