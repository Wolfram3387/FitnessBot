import re
from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from data.message_texts import *
from states import AddingWorkout
from keyboards.default.all import cancel


@dp.message_handler(state=AddingWorkout.input_date)
async def input_date(message: types.Message, state: FSMContext):
    if message.text == cancel.keyboard[-1][-1].text:
        return await state.finish()
    if not re.match(
            (r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)('
             r'?:0?[1,3-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|'
             r'-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579]'
             r'[26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2'
             r'[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d'
             r')?\d{2})$'), message.text
    ):
        return await message.answer(INCORRECT_DATE)
    await AddingWorkout.input_workout.set()
    await message.answer(SEND_WORKOUT)
    await state.update_data(date=message.text)


@dp.message_handler(state=AddingWorkout.input_workout)
async def input_workout(message: types.Message, state: FSMContext):
    if message.text == cancel.keyboard[-1][-1].text:
        return await state.finish()
    try:
        data = await state.get_data()
        date = data.get('date')
        db.add_workout(id_=message.from_user.id, workout=message.text, date=date)
    except:
        return await message.answer(SOMETHING_WENT_WRONG)
    await message.answer(WORKOUT_SUCCESS)
    await state.finish()
