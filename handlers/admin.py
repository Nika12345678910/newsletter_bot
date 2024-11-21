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
from FSM.fsm import AddScheduleFSM, AddFloorFSM, ChangeRoomsFSM
from filter.filter import DateFilter, TimeFilter, NumbersRoomsFilter
from database.query_orm import (get_rooms_orm,
                                add_schedule_orm,
                                get_room_orm,
                                get_id_chats_orm,
                                get_user_orm,
                                add_floor_orm,
                                get_id_floor_orm,
                                add_rooms_orm,
                                get_rooms_row_orm,
                                get_floor_orm,
                                get_rooms_floor_orm,
                                get_id_floor_orm2,
                                delete_rooms_orm)


admin_router = Router()

admin_kb = create_keyboard(btns["possibilities_admin"],
                           placeholder=btns["placeholder_admin_kb"])


@admin_router.message(Command(commands=['admin']), StateFilter(default_state))
async def command_admin(message: Message, session: AsyncSession, state: FSMContext):
    if await get_user_orm(session, int(message.from_user.id)):
        await message.answer(text=f'{LEXICON["admin"]}, {message.from_user.first_name}',
                             reply_markup=admin_kb)
        return

    ids_chats_headmen = [floor_obj.id_chat_headmen for floor_obj in await get_floor_orm(session)]
    if message.from_user.id not in ids_chats_headmen:
        await message.answer(text=LEXICON["add_floor"])
        await state.set_state(AddFloorFSM.floor)
        return

    await message.answer(text=LEXICON["registration_admin"],
                         reply_markup=get_callback_btns(btns=btns["registation"]))


#Добавление этажа и комнат
@admin_router.message(AddFloorFSM.floor, F.text.isdigit())
async def add_floor(message: Message, state: FSMContext):
    await state.update_data(floor=int(message.text))
    await message.answer(text=LEXICON["add_numbers_rooms"])
    await state.set_state(AddFloorFSM.numbers_rooms)


@admin_router.message(NumbersRoomsFilter(), AddFloorFSM.numbers_rooms, F.text)
async def add_numbers_rooms(message: Message, state: FSMContext, session: AsyncSession):
    rooms = [str(i) for i in message.text.replace(' ', ',').replace(',,', ',').split(',')]
    await state.update_data(numbers_rooms=rooms)
    data = await state.get_data()

    data_floor_table = {
        "number_floor": int(data["floor"]),
        "id_chat_headmen": message.from_user.id
    }
    await add_floor_orm(session, data_floor_table)

    id_floor = await get_id_floor_orm(session, int(data["floor"]))
    await add_rooms_orm(session, id_floor, data["numbers_rooms"],)

    await state.clear()
    await message.answer(text=LEXICON["add_data_headmen"])


@admin_router.message(AddFloorFSM.floor)
async def add_floor2(message: Message):
    await message.answer(text=LEXICON["error_floor"])


@admin_router.message(AddFloorFSM.numbers_rooms)
async def add_floor2(message: Message):
    await message.answer(text=LEXICON["error_numbers_rooms"])


#Добавление/изменение комнат этажа
@admin_router.message(F.text == "Добавление/изменение комнат этажа", StateFilter(default_state))
async def change_rooms(message: Message, session: AsyncSession, state: FSMContext):
    id_floor = await get_id_floor_orm2(session, message.from_user.id)
    rooms_on_floor = await get_rooms_floor_orm(session, id_floor)

    await message.answer(text=LEXICON["change_rooms"],
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(text=", ".join(rooms_on_floor),
                         reply_markup=get_callback_btns(btns=btns["cancel"]))
    await state.set_state(ChangeRoomsFSM.rooms)


@admin_router.message(ChangeRoomsFSM.rooms, NumbersRoomsFilter())
async def change_rooms2(message: Message, session: AsyncSession, state: FSMContext):
    id_floor = await get_id_floor_orm2(session, message.from_user.id)
    old_rooms = await get_rooms_floor_orm(session, id_floor)

    new_rooms = [str(i) for i in message.text.replace(' ', ',').replace(',,', ',').split(',')]

    #комнаты которые есть в новом но нет в старом (добавить)
    dif1 = set(new_rooms) - set(old_rooms)
    rooms_to_add = [room for room in dif1]
    try:
        await add_rooms_orm(session, id_floor, rooms_to_add)
    except Exception as e:
        await message.answer(f"Ошибка: \n{str(e)}\nЧто-то пошло не так при добавлении новых комнат в БД",
                             reply_markup=admin_kb)

    #комнаты которые есть в старом но нет в новом (удалить)
    dif2 = set(old_rooms) - set(new_rooms)
    for room in dif2:
        try:
            await delete_rooms_orm(session, room)
        except Exception as e:
            await message.answer(f"Ошибка \n{str(e)}\nЧтото- пошло не так при удалении старых комнат из БД",
                                 reply_markup=admin_kb)
    await state.clear()
    await message.answer(text=LEXICON["add_data_headmen"],
                         reply_markup=admin_kb)


#Создание расписания
@admin_router.message(F.text == "Создание расписания", StateFilter(default_state))
async def create_schedule(message: Message, state: FSMContext):
    await message.answer(text=LEXICON["start_create_schedule"],
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(text=LEXICON["date"],
                         reply_markup=get_callback_btns(btns=btns["cancel"]))
    await state.set_state(AddScheduleFSM.date)


@admin_router.message(DateFilter(), AddScheduleFSM.date)
async def add_date(message: Message, state: FSMContext):
    soo = message.text.split('-')
    var_date = date(int(soo[0]), int(soo[1]), int(soo[2]))

    await state.update_data(date=var_date)
    await message.answer(text=LEXICON["time"],
                         reply_markup=get_callback_btns(btns=btns["cancel"]))
    await state.set_state(AddScheduleFSM.time)


@admin_router.message(TimeFilter(), AddScheduleFSM.time)
async def add_time(message: Message, state: FSMContext, session: AsyncSession):
    rooms = await get_rooms_orm(session)

    soo = message.text.split(':')
    var_time = time(int(soo[0]), int(soo[1]), 0)

    await state.update_data(time=var_time)
    await message.answer(text=f'{LEXICON["room"]}: {", ".join(rooms)}',
                         reply_markup=get_callback_btns(btns=btns["cancel"]))
    await state.set_state(AddScheduleFSM.room)


@admin_router.message(AddScheduleFSM.room)
async def add_room(message: Message, session: AsyncSession, state: FSMContext):
    await state.update_data(room=int(message.text))

    data = await state.get_data()
    schedule = format_schedule(data["date"], data["time"], message.text)

    btns = check_schedule_kb(data) #кнопки для инлайн клавиатуры для подтверждения/изменения расписания

    await message.answer(text=f'{LEXICON["check_schedule"]}\n{schedule}',
                                  reply_markup=get_callback_btns(btns=btns))
    await state.clear()


@admin_router.message(AddScheduleFSM.date)
async def add_date2(message: Message):
    await message.answer(text=LEXICON["error_date"])


@admin_router.message(AddScheduleFSM.time)
async def add_time2(message: Message):
    await message.answer(text=LEXICON["error_time"])


@admin_router.message(AddScheduleFSM.room)
async def add_room2(message: Message):
    await message.answer(text=LEXICON["error_room"])


#Рассылка расписания пользователям
async def newsletter_schedule(session: AsyncSession,
                              bot: Bot,
                              data_ids_floors: dict,
                              data_rooms: dict,
                              schedule: str,
                              cleaning_room: str) -> None:
    id_chats = await get_id_chats_orm(session)
    cleaning_id_room = data_rooms[cleaning_room][0] #id комнаты, которая убирается
    id_floor = data_rooms[cleaning_room][1] #id этажа, жителям которого приходит рассылка


    for id_chat in id_chats:
        user_data = await get_user_orm(session, id_chat)
        id_room_user = user_data.id_room
        id_floor_user = data_ids_floors[str(id_room_user)]

        if id_floor_user == id_floor:
            await bot.send_message(id_chat, text=schedule)


async def data_unpacking(data: list) -> tuple:
    #дата уборки
    input_date = data[1].split('-')
    cleaning_date = date(int(input_date[0]), int(input_date[1]), int(input_date[2]))
    #время уборки
    input_time = data[2].split(':')
    cleaning_time = time(int(input_time[0]), int(input_time[1]), 0)
    #номер комнаты, которая убирается (обозначили для понимания)
    cleaning_room = data[3]

    return cleaning_date, cleaning_time, cleaning_room


#Публикация расписания
@admin_router.callback_query(F.data.startswith("confirm_"))
async def public_schedule(callback: CallbackQuery, session: AsyncSession, bot: Bot):
    data = callback.data.split('_')

    cleaning_date, cleaning_time, cleaning_room = await data_unpacking(data)
    schedule = format_schedule(cleaning_date, cleaning_time, cleaning_room)

    data_rooms = {str(room.number): [room.id, room.id_floor] for room in await get_rooms_row_orm(session)}
    data_ids_floors = {str(room.id): room.id_floor for room in await get_rooms_row_orm(session)}

    data_Schedule = {"date": cleaning_date,
                     "time": cleaning_time,
                     "id_room": data_rooms[cleaning_room][0]} #id комнаты, которая убирается

    try:
        await add_schedule_orm(session, data_Schedule)
        await callback.answer()
    except Exception as e:
        await callback.message.answer(
            f"Ошибка: \n{str(e)}\nЧто-то пошло не так при добавлении расписания в БД",
            reply_markup=admin_kb)

    try:
        await newsletter_schedule(session=session,
                                  bot=bot,
                                  data_rooms=data_rooms,
                                  data_ids_floors=data_ids_floors,
                                  schedule=schedule,
                                  cleaning_room=cleaning_room)

        await callback.message.answer(text=f'{LEXICON["public_schedule"]}',
                                      reply_markup=admin_kb)
        await callback.answer()
    except Exception as e:
        await callback.message.answer(f"Ошибка: \n{str(e)}\nЧто-то пошло не так во время рассылки расписания жителям этажа",
                                      reply_markup=admin_kb)
        await callback.answer()



#Изменение расписания
@admin_router.callback_query(F.data.startswith("change_"), StateFilter(default_state))
async def change_schedule(callback: CallbackQuery, state: FSMContext):
    await create_schedule(callback.message, state)
    await callback.answer(text=LEXICON["change_schedule"])


#Отмена действий по создания расписания
@admin_router.callback_query(F.data == "cancel")
async def cancel_move(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await callback.answer()
    await state.clear()
    await callback.message.answer("Действия отменены", reply_markup=admin_kb)


#Главное меню
@admin_router.message(F.text == "Главное меню")
async def main_menu(message: Message):
    await message.answer(text=LEXICON["possibilities_user"],
                                  reply_markup=get_callback_btns(btns=btns["possibilities_user"]))