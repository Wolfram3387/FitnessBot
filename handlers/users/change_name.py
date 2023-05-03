from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from states import SetName
from data.message_texts import *
from keyboards.default.all import cancel


@dp.message_handler(state=SetName.set_name)
async def input_name(message: types.Message, state: FSMContext):
    if message.text == cancel.keyboard[-1][-1].text:
        return await state.finish()
    if not 1 < len(message.text) < 50:
        return await message.answer(NAME_IS_INVALID)
    try:
        db.update_name(id_=message.from_user.id, name=message.text)
        await state.finish()
        await message.answer(NAME_SET_SUCCESS.format(name=message.text))
    except:
        await message.answer(SOMETHING_WENT_WRONG)
