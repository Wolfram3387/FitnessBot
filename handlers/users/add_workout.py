from aiogram import types
from loader import dp
from states import AddingWorkout


@dp.message_handler(state=AddingWorkout.input_date)
async def input_date(message: types.Message):
    pass


@dp.message_handler(state=AddingWorkout.input_workout)
async def input_workout(message: types.Message):
    pass
