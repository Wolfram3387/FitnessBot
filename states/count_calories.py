from aiogram.dispatcher.filters.state import StatesGroup, State


class CountCalories(StatesGroup):
    input_gender = State()
    input_age = State()
    input_weight = State()
    input_height = State()
    input_activity_degree = State()
