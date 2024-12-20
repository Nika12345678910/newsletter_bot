from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from types import NoneType

from database.query_orm import get_rooms_orm, get_floor_orm
from lexicon.lexicon_ru import LEXICON, btns
from keyboard.inline import get_callback_btns

from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime


class DateFilter(BaseFilter):
    async def __call__(self, message: Message):
        test = message.text.replace("-", "")

        if len(message.text.split('-'))==3 and len(test) == 8 and test.isdigit():
            test1 = 0<int(test[6:])<32 and 0<int(test[4:6])<13
            test2 = message.text[0]!='-' and message.text[-1]!='-'
            test3 = datetime.now().year == int(test[:4])
            test4 = datetime.now().month == int(test[4:6]) and int(str(datetime.today())[8:10]) <= int(test[6:]) < 32
            test5 = int(test[4:6]) == datetime.now().month+1 and int(str(datetime.today())[8:10]) >= int(test[6:]) >= 1

            if test1 and test2 and test3:
                if test4 or test5:
                    return True
                return False
            return False
        return False


class TimeFilter(BaseFilter):
    async def __call__(self, message: Message):
        test = message.text.replace(":", "")
        if (len(test) == 4 and test.isdigit() and
            0<=int(test[:2])<=24 and 0<=int(test[2:])<=24 and
            message.text[0]!=':' and message.text[-1]!=':'
            and len(message.text.split(":"))==2):
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
    async def __call__(self, message: Message, session: AsyncSession, state: FSMContext):
        rooms = await get_rooms_orm(session)
        if message.text in rooms:
            return True
        if len(rooms) == 0:
            await message.answer(text=LEXICON["not rooms"],
                                 reply_markup=get_callback_btns(btns=btns["registation"]))
            await state.clear()
        return
