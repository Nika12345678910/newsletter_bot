from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage


storage = MemoryStorage()


class UserDataFSM(StatesGroup):
    first_name = State()
    last_name = State()
    room = State()


class AddScheduleFSM(StatesGroup):
    date = State()
    time = State()
    room = State()


class AddFloorFSM(StatesGroup):
    floor = State()
    numbers_rooms = State()