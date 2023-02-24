from aiogram import types
from loader import dp
from states import CountCalories


@dp.message_handler(state=CountCalories.input_gender)
async def input_gender(message: types.Message):
    pass


@dp.message_handler(state=CountCalories.input_weight)
async def input_weight(message: types.Message):
    pass


@dp.message_handler(state=CountCalories.input_height)
async def input_height(message: types.Message):
    pass


@dp.message_handler(state=CountCalories.input_age)
async def input_age(message: types.Message):
    pass


@dp.message_handler(state=CountCalories.input_activity_degree)
async def input_activity_degree(message: types.Message):
    pass
