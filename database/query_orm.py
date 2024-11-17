import logging
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from database.models import Users, Rooms, Schedule


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
    query = select(Users).where(Users.id_chat==id_chat)
    result = await session.execute(query)
    return result.scalars().all()


#Rooms
async def add_rooms_orm(session: AsyncSession, data: list):
    query = select(Rooms)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([Rooms(room=room) for room in data])
    await session.commit()


async def get_rooms_orm(session: AsyncSession):
    query = select(Rooms)
    result = await session.execute(query)
    return result.scalars().all()


#Schedule
