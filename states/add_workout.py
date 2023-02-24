from aiogram.dispatcher.filters.state import StatesGroup, State


class AddingWorkout(StatesGroup):
    input_date = State()
    input_workout = State()
