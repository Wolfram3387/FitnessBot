from aiogram.dispatcher.filters.state import StatesGroup, State


class CountBMI(StatesGroup):
    input_weight = State()
    input_height = State()
