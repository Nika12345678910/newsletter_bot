from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from types import NoneType

from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon_ru import (LEXICON, btns,
                                format_profile,
                                format_schedule,
                                format_user_schedule_confirmation)
from FSM.fsm import UserDataFSM, ViewScheduleFSM
from database.query_orm import (add_user_orm,
                                get_user_orm,
                                get_rooms_orm,
                                get_room_orm,
                                get_rooms_row_orm,
                                get_schedule_orm,
                                get_schedules_orm,
                                get_floor_orm,
                                get_id_chats_orm)
from keyboard.inline import get_callback_btns
from filter.filter import NameFilter, RoomFilter, DateFilter


user_router = Router()


@user_router.message(CommandStart())
async def command_start(message: Message, session: AsyncSession):
    await message.answer(f'{LEXICON["start"]}, {message.from_user.first_name}')
    if message.from_user.id in await get_id_chats_orm(session):
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

    await state.update_data(last_name=message.text)
    await message.answer(text=f'{LEXICON["room"]}: {", ".join(rooms)}')
    await state.set_state(UserDataFSM.room)


@user_router.message(UserDataFSM.room, RoomFilter())
async def add_room(message: Message, session: AsyncSession, state: FSMContext):
    await state.update_data(room=int(message.text))

    data = await state.get_data()

    rooms = {str(room.number): room.id for room in await get_rooms_row_orm(session)}
    data["id_room"] = rooms[message.text]
    data["id_chat"] = message.from_user.id
    try:
        await add_user_orm(session, data)
        await message.answer(text=LEXICON["registration_close"])
        await message.answer(text=LEXICON["possibilities_user"],
                                      reply_markup=get_callback_btns(btns=btns["possibilities_user"]))
        await state.clear()
    except Exception as e:
        await message.answer(
            f"Ошибка: \n{str(e)}\nЧто-то пошло не так при добавлении данных пользователя в БД",
            reply_markup=get_callback_btns(btns=btns["registation"]),
        )
        await state.clear()


@user_router.message(UserDataFSM.first_name)
async def add_first_name2(messagge: Message, state: FSMContext):
    await messagge.answer(text=LEXICON["error_first_name"])


@user_router.message(UserDataFSM.last_name)
async def add_last_name2(messagge: Message, state: FSMContext):
    await messagge.answer(text=LEXICON["error_last_name"])


@user_router.message(UserDataFSM.room)
async def add_room2(messagge: Message, state: FSMContext):
    await messagge.answer(text=LEXICON["error_room"])


#Просмотр профиля
@user_router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery, session: AsyncSession):
    user_data = await get_user_orm(session, int(callback.from_user.id))
    room = await get_room_orm(session, user_data.id_room)
    profile = format_profile(user_data.first_name, user_data.last_name, room.number)
    await callback.message.answer(text=profile,
                                  reply_markup=get_callback_btns(btns=btns["main_menu"]))


#Просмотр расписания
@user_router.callback_query(F.data == "view schedule", StateFilter(default_state))
async def view_schedule(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    dates = [str(date) for date in await get_schedules_orm(session)]

    await callback.message.answer(text=f'{LEXICON["view_schedule"]}: {", ".join(dates)}',
                                  reply_markup=get_callback_btns(btns=btns["main_menu"]))
    await state.set_state(ViewScheduleFSM.date)
    await callback.answer()


@user_router.message(ViewScheduleFSM.date, DateFilter())
async def chande_date_schedule(message: Message, session: AsyncSession, state: FSMContext):
    cleaning_date = date(int(message.text[:4]), int(message.text[5:7]), int(message.text[8:10]))
    data_schedule = await get_schedule_orm(session, cleaning_date)

    if type(data_schedule) == NoneType:
        await message.answer(text=LEXICON["not date"],
                             reply_markup=get_callback_btns(btns=btns["main_menu"]))
        await state.clear()
        return

    room = await get_room_orm(session, data_schedule.id_room)
    schedule = format_schedule(data_schedule.date, data_schedule.time, room.number)
    await message.answer(text=schedule,
                         reply_markup=get_callback_btns(btns=btns["main_menu"]))
    await state.clear()


@user_router.message(ViewScheduleFSM.date)
async def chande_date_schedule(message: Message, session: AsyncSession):
    dates = [str(date) for date in await get_schedules_orm(session)]
    await message.answer(text=f'{LEXICON["view_schedule"]}: {", ".join(dates)}')


#Вывод главного меню
@user_router.callback_query(F.data == "main_menu")
async def output_main_menu(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON["possibilities_user"],
                                  reply_markup=get_callback_btns(btns=btns["possibilities_user"]))
    await callback.answer()


#Подтверждение расписания пользователем
@user_router.callback_query(F.data.startswith("confirm_schedule_"))
async def process_confirm_schedule(callback: CallbackQuery, session: AsyncSession, bot: Bot):
    input_data = callback.data.split('_')
    date = input_data[-3]
    id_chat_user = int(input_data[-2])
    id_floor_user = input_data[-1]

    #Найти: имя, фамилию и комнату подтвердившего юзера
    #Найти ид чата старосты этажа

    data_user = await get_user_orm(session, id_chat_user)
    room_obj_user = await get_room_orm(session, data_user.id_room)
    ids_chats_headmen = {str(floor_obj.id): floor_obj.id_chat_headmen for floor_obj in await get_floor_orm(session)}
    id_chat_headmen = ids_chats_headmen[id_floor_user]

    report = format_user_schedule_confirmation(data_user.first_name,
                                               data_user.last_name,
                                               room_obj_user.number,
                                               date)

    await bot.send_message(chat_id=id_chat_headmen, text=report)