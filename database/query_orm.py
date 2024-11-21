import logging

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from datetime import date

from database.models import Users, Rooms, Schedule, Floors


#Users
async def add_user_orm(session: AsyncSession, data: dict):
    user = Users(
        id_chat=data["id_chat"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        id_room=data["id_room"]
    )
    session.add(user)
    await session.commit()


async def get_user_orm(session: AsyncSession, id_chat: int):
    query = select(Users).where(Users.id_chat == id_chat)
    result = await session.execute(query)
    return result.scalar()


async def get_id_chats_orm(session: AsyncSession):
    query = select(Users.id_chat)
    result = await session.execute(query)
    return result.scalars().all()


#Rooms
async def add_rooms_orm(session: AsyncSession, id_floor: int, rooms: list):
    query = select(Rooms)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([Rooms(number=number, id_floor=id_floor) for number in rooms])
    await session.commit()


async def get_rooms_orm(session: AsyncSession):
    query = select(Rooms.number)
    result = await session.execute(query)
    return result.scalars().all()


async def get_room_orm(session: AsyncSession, id_room: int):
    query = select(Rooms).where(Rooms.id == id_room)
    result = await session.execute(query)
    return result.scalar()


async def get_rooms_row_orm(session: AsyncSession):
    query = select(Rooms)
    result = await session.execute(query)
    return result.scalars().all()


async def get_rooms_floor_orm(session: AsyncSession, id_floor: int):
    query = select(Rooms.number).where(Rooms.id_floor == id_floor)
    result = await session.execute(query)
    return result.scalars().all()


async def delete_rooms_orm(session: AsyncSession, number: int):
    query = delete(Rooms).where(Rooms.number == number)
    await session.execute(query)
    await session.commit()


#Schedule
async def add_schedule_orm(session: AsyncSession, data: dict):
    schedule = Schedule(
        time=data["time"],
        date=data["date"],
        id_room=data["id_room"]
    )
    session.add(schedule)
    await session.commit()


async def get_schedule_orm(session: AsyncSession, date: date):
    query = select(Schedule).where(Schedule.date==date)
    result = await session.execute(query)
    return result.scalar()


async def get_schedules_orm(session: AsyncSession):
    query = select(Schedule.date)
    result = await session.execute(query)
    return result.scalars().all()


#Floors
async def add_floor_orm(session: AsyncSession, data: dict):
    floor = Floors(
        number_floor=data["number_floor"],
        id_chat_headmen=data["id_chat_headmen"]
    )
    session.add(floor)
    await session.commit()


async def get_id_floor_orm(session: AsyncSession, floor: int):
    query = select(Floors.id).where(Floors.number_floor == floor)
    result = await session.execute(query)
    return result.scalar()


async def get_floor_orm(session: AsyncSession):
    query = select(Floors)
    result = await session.execute(query)
    return result.scalars().all()


async def get_id_floor_orm2(session: AsyncSession, id_chat_headmen: int):
    query = select(Floors.id).where(Floors.id_chat_headmen == id_chat_headmen)
    result = await session.execute(query)
    return result.scalar()