import os
import xlsxwriter
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import \
    CommandStart, CommandHelp, Command

from loader import dp
from states import AddingWorkout, CountCalories, CountBMI
from utils.misc import rate_limit
from data.message_texts import *


@rate_limit(5, 'start')
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f'Привет, {message.from_user.full_name}!')
    # TODO db.add_sportsman(id_=message.from_user.id, name=message.from_user.name)


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/set_name - Сменить своё имя'
        '/add_workout - Запись новой тренировки',
        '/calories - Рассчитать дневную норму калорий',
        '/bmi - Рассчитать индекс массы тела',
        '/export - Сохранить все свои тренировки в файл',
    ]
    await message.answer('\n'.join(text))


@rate_limit(5, 'add_workout')
@dp.message_handler(Command('add_workout'))
async def add_workout(message: types.Message):
    await AddingWorkout.input_date.set()
    await message.answer(ADD_WORKOUT)
    await message.answer(SEND_WORKOUT_DATE)


@rate_limit(5, 'calories')
@dp.message_handler(Command('calories'))
async def count_calories(message: types.Message):
    await CountCalories.input_gender.set()
    await message.answer(ABOUT_CALORIES)
    await message.answer(SELECT_GENDER)


@rate_limit(5, 'bmi')
@dp.message_handler(Command('bmi'))
async def count_bmi(message: types.Message):
    await CountBMI.input_gender.set()
    await message.answer(ABOUT_BMI)
    await message.answer(SELECT_GENDER)


@rate_limit(5, 'set_name')
@dp.message_handler(Command('set_name'))
async def set_name(message: types.Message):
    if not 1 < len(message.text) < 50:
        return await message.answer('Имя должно быть от 1 до 50 символов')
    try:
        # TODO update name in db
        await message.answer(NAME_SET_SUCCESS.format(name=message.text))
    except:
        await message.answer(SOMETHING_WENT_WRONG)


@rate_limit(5, 'export')
@dp.message_handler(Command('export'))
async def to_excel(message: types.Message):
    await message.answer('Собираю данные...')
    workouts = []
    # TODO workouts = db.get_all_workouts()
    name = 'qwerty'
    # TODO name = db.get_name(id_=message.from_user.id)
    path = f'export/{name}.xlsx'
    if os.path.exists(path):
        path = f'export/{message.from_user.id}.xlsx'

    with xlsxwriter.Workbook(path) as workbook:
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, 'Дата')
        worksheet.write(0, 1, 'Тренировка')

        for row_number, item in enumerate(workouts, start=1):
            worksheet.write(row_number, 0, item[2])
            worksheet.write(row_number, 1, item[1])

    await message.answer_document(
        document=open(path),
        caption=f'{name}, вот все твои тренировки'
    )
    os.remove(path)
