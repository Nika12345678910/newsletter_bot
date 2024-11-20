from aiogram.filters import BaseFilter
from aiogram.types import Message
from database.query_orm import get_rooms_orm
from sqlalchemy.ext.asyncio import AsyncSession


class DateFilter(BaseFilter):
    async def __call__(self, message: Message):
        test = message.text.replace("/", "")
        if (len(test) == 8 and test.isdigit() and
            0<int(test[6:])<32 and 0<int(test[4:6])<13 and
            message.text[0]!='/' and message.text[-1]!='/'):
            return True
        else:
            return False


class TimeFilter(BaseFilter):
    async def __call__(self, message: Message):
        test = message.text.replace(":", "")
        if (len(test) == 4 and test.isdigit() and
            0<=int(test[:2])<=24 and 0<=int(test[2:])<=24 and
            message.text[0]!=':' and message.text[-1]!=':'):
            return True
        else:
            return False


class NameFilter(BaseFilter):
    async def __call__(self, message: Message):
        for i in message.text:
            if 1040 > ord(i) or ord(i) > 1103:
                return False
        return True


class NumbersRoomsFilter(BaseFilter):
    async def __call__(self, message: Message):
        soo = message.text.replace(' ', ',').replace(',,', ',').split(',')
        for i in soo:
            if not(i.isdigit()):
                return False
        if len(soo) == len(set(soo)):
            return True
        else:
            return False


class RoomFilter(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession):
        rooms = await get_rooms_orm(session)
        if message.text in rooms:
            return True
        return False