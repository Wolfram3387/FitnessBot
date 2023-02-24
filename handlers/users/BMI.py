from aiogram import types
from loader import dp
from states import CountBMI


@dp.message_handler(state=CountBMI.input_weight)
async def input_weight(message: types.Message):
    pass


@dp.message_handler(state=CountBMI.input_height)
async def input_height(message: types.Message):
    pass
