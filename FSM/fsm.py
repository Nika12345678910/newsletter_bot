from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage


storage = MemoryStorage()


class UserDataFSM(StatesGroup):
    first_name = State()
    last_name = State()
    id_room = State()


class AddScheduleFSM(StatesGroup):
    date = State()
    time = State()
    id_room = State()