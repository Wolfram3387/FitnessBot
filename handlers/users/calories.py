from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states import CountCalories
from data.message_texts import *


@dp.message_handler(state=CountCalories.input_gender)
async def input_gender(message: types.Message, state: FSMContext):
    if message.text == '':  # TODO написать текст кнопки ОТМЕНА
        return await state.finish()
    if message.text not in []:  # TODO перечислить текст кнопок м/ж
        return await message.answer(SELECT_GENDER)
    await CountCalories.next()
    await message.answer(SEND_WEIGHT)
    await state.update_data(gender=message.text)


@dp.message_handler(state=CountCalories.input_weight)
async def input_weight(message: types.Message, state: FSMContext):
    if message.text == '':  # TODO написать текст кнопки ОТМЕНА
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
    if message.text == '':  # TODO написать текст кнопки ОТМЕНА
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
    if message.text == '':  # TODO написать текст кнопки ОТМЕНА
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
    return 0


@dp.message_handler(state=CountCalories.input_activity_degree)
async def input_activity_degree(message: types.Message, state: FSMContext):

    # Проверяем ввод
    if message.text == '':  # TODO написать текст кнопки ОТМЕНА
        return await state.finish()
    if message.text not in []:  # TODO перечислить текст кнопок выбора активности
        return await message.answer(SELECT_ACTIVITY_DEGREE)

    # Получаем введённые данные
    gender = await state.get_data('gender')
    weight = await state.get_data('weight')
    height = await state.get_data('height')
    age = await state.get_data('age')
    activity_degree = message.text

    # Считаем суточную норму калорий
    calories = get_daily_calories(gender, weight, height, age, activity_degree)

    # Отправляем результат
    await state.finish()
    five_percents = round(calories * 0.05)
    await message.answer(CALORIES_RESULT.format(
        start=calories-five_percents,
        end=calories+five_percents)
    )
