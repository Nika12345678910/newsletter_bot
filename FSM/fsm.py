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


class AdminStartFSM(StatesGroup):
    registration = State()
    add_floor = State()
    admin_menu = State()


class ViewScheduleFSM(StatesGroup):
    date = State()


class ChangeRoomsFSM(StatesGroup):
    rooms = State()