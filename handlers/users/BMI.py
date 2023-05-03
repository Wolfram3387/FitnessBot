from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states import CountBMI
from data.message_texts import *
from keyboards.default.all import cancel, genders


@dp.message_handler(state=CountBMI.input_gender)
async def input_gender(message: types.Message, state: FSMContext):
    if message.text == cancel.keyboard[-1][-1].text:
        await message.answer(CANCELED, reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        return None
    if message.text not in [btn['text'] for btn in genders.keyboard[-1]]:
        return await message.answer(SELECT_GENDER)
    await CountBMI.next()
    await message.answer(SEND_WEIGHT, reply_markup=cancel)
    await state.update_data(gender=message.text)


@dp.message_handler(state=CountBMI.input_weight)
async def input_weight(message: types.Message, state: FSMContext):
    if message.text == cancel.keyboard[-1][-1].text:
        await message.answer(CANCELED, reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        return None
    try:
        weight = float(message.text.replace(',', '.'))
    except TypeError:
        return await message.answer('Введите число')
    if not 1 < weight < 700:
        return await message.answer('Введите реальное значение')
    await CountBMI.next()
    await message.answer(SEND_HEIGHT, reply_markup=cancel)
    await state.update_data(weight=weight)


@dp.message_handler(state=CountBMI.input_height)
async def input_height(message: types.Message, state: FSMContext):
    if message.text == cancel.keyboard[-1][-1].text:
        await message.answer(CANCELED, reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        return None
    try:
        height = float(message.text.replace(',', '.')) / 100
    except TypeError:
        return await message.answer('Введите число')
    if not 1 < height < 250:
        return await message.answer('Введите реальное значение')
    data = await state.get_data()
    gender = data.get('gender')
    weight = data.get('weight')
    bmi = round(weight / height ** 2, 2)
    await state.finish()
    if gender == genders.keyboard[-1][0]['text']:
        await message.answer_photo(open('data/BMI_male.png', 'rb'))
    else:
        await message.answer_photo(open('data/BMI_female.png', 'rb'))
    await message.answer(BMI_RESULT.format(bmi=bmi), reply_markup=types.ReplyKeyboardRemove())
