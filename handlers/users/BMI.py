from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states import CountBMI
from data.message_texts import *
from keyboards.default.all import cancel, genders


@dp.message_handler(state=CountBMI.input_gender)
async def input_gender(message: types.Message, state: FSMContext):
    if message.text == cancel.keyboard[-1][-1].text:
        return await state.finish()
    if message.text not in [btn['text'] for btn in genders.keyboard[-1]]:
        return await message.answer(SELECT_GENDER)
    await CountBMI.next()
    await message.answer(SEND_WEIGHT)
    await state.update_data(gender=message.text)


@dp.message_handler(state=CountBMI.input_weight)
async def input_weight(message: types.Message, state: FSMContext):
    if message.text == cancel.keyboard[-1][-1].text:
        return await state.finish()
    if not message.text.isdigit():
        return await message.answer('Введите число')
    if not 1 < int(message.text) < 700:
        return await message.answer('Введите реальное значение')
    await CountBMI.next()
    await message.answer(SEND_HEIGHT)
    await state.update_data(weight=int(message.text))


@dp.message_handler(state=CountBMI.input_height)
async def input_height(message: types.Message, state: FSMContext):
    if message.text == cancel.keyboard[-1][-1].text:
        return await state.finish()
    if not message.text.isdigit():
        return await message.answer('Введите число')
    if not 1 < int(message.text) < 250:
        return await message.answer('Введите реальное значение')
    gender = await state.get_data('gender')
    weight = await state.get_data('weight')
    height = int(message.text)
    bmi = round(weight / (height ** 2), 2)
    await state.finish()
    if gender == genders.keyboard[-1][0]['text']:
        await message.answer_document(open('data/BMI_male.webp'))
    else:
        await message.answer_document(open('data/BMI_female.webp'))
    await message.answer(BMI_RESULT.format(bmi=bmi))
