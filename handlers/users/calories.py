from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.all import cancel, genders, activity_degrees
from loader import dp
from states import CountCalories
from data.message_texts import *


@dp.message_handler(state=CountCalories.input_gender)
async def input_gender(message: types.Message, state: FSMContext):
    if message.text == cancel.keyboard[-1][-1].text:
        return await state.finish()
    if message.text not in [btn['text'] for btn in genders.keyboard[-1]]:
        return await message.answer(SELECT_GENDER)
    await CountCalories.next()
    await message.answer(SEND_WEIGHT)
    await state.update_data(gender=message.text)


@dp.message_handler(state=CountCalories.input_weight)
async def input_weight(message: types.Message, state: FSMContext):
    if message.text == cancel.keyboard[-1][-1].text:
        return await state.finish()
    if not message.text.isdigit():
        return await message.answer('Введите число')
    if not 1 < int(message.text) < 700:
        return await message.answer('Введите реальное значение')
    await CountCalories.next()
    await message.answer(SEND_HEIGHT)
    await state.update_data(weight=int(message.text))


@dp.message_handler(state=CountCalories.input_height)
async def input_height(message: types.Message, state: FSMContext):
    if message.text == cancel.keyboard[-1][-1].text:
        return await state.finish()
    if not message.text.isdigit():
        return await message.answer('Введите число')
    if not 1 < int(message.text) < 250:
        return await message.answer('Введите реальное значение')
    await CountCalories.next()
    await message.answer(SEND_AGE)
    await state.update_data(height=int(message.text))


@dp.message_handler(state=CountCalories.input_age)
async def input_age(message: types.Message, state: FSMContext):
    if message.text == cancel.keyboard[-1][-1].text:
        return await state.finish()
    if not message.text.isdigit():
        return await message.answer('Введите число')
    if not 1 < int(message.text) < 120:
        return await message.answer('Введите реальное значение')
    await CountCalories.next()
    await message.answer(SELECT_ACTIVITY_DEGREE)
    await state.update_data(age=int(message.text))


def get_daily_calories(gender, weight, height, age, activity_degree) -> int:
    """Вычисляет суточную норму калорий"""

    # men
    if gender == genders.keyboard[-1][0]['text']:
        bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)

    # women
    else:
        bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)

    keys = [btn[0]['text'] for btn in activity_degrees.keyboard]
    values = [1.2, 1.375, 1.55, 1.725, 1.9]
    degree_transfer = dict(zip(keys, values))

    return bmr * degree_transfer[activity_degree]


@dp.message_handler(state=CountCalories.input_activity_degree)
async def input_activity_degree(message: types.Message, state: FSMContext):

    # Проверяем ввод
    if message.text == cancel.keyboard[-1][-1].text:
        return await state.finish()
    if message.text not in [btn[0]['text'] for btn in activity_degrees.keyboard]:
        return await message.answer(SELECT_ACTIVITY_DEGREE)

    # Получаем введённые данные
    gender = await state.get_data('gender')
    weight = await state.get_data('weight')
    height = await state.get_data('height')
    age = await state.get_data('age')
    activity_degree = message.text

    # Считаем суточную норму калорий
    daily_calories = get_daily_calories(gender, weight, height, age, activity_degree)

    # Отправляем результат
    await state.finish()
    five_percents = round(daily_calories * 0.05)
    await message.answer(CALORIES_RESULT.format(
        start=daily_calories-five_percents,
        end=daily_calories+five_percents)
    )
