from aiogram.dispatcher.filters.state import StatesGroup, State


class SetName(StatesGroup):
    set_name = State()
