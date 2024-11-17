import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from database.models import Base
from config_data.config import load_config
from lexicon.lexicon_ru import btns
from database.query_orm import add_rooms_orm


url_db = load_config().db.create_url()

engine = create_async_engine(url=url_db, echo=False)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with session_maker() as session:
        await add_rooms_orm(session, btns["rooms"])


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)