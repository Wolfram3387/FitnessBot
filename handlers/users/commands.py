from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp, Command

from loader import dp
from states import AddingWorkout, CountCalories, CountBMI
from utils.misc import rate_limit


@rate_limit(5, 'start')
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!')
    ...


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/help - Получить справку'
    ]
    await message.answer('\n'.join(text))


@rate_limit(5, 'add_workout')
@dp.message_handler(Command('add_workout'))
async def add_workout(message: types.Message):
    await AddingWorkout.input_date.set()
    ...


@rate_limit(5, 'calories')
@dp.message_handler(Command('calories'))
async def count_calories(message: types.Message):
    await CountCalories.input_gender.set()
    ...


@rate_limit(5, 'bmi')
@dp.message_handler(Command('bmi'))
async def count_bmi(message: types.Message):
    await CountBMI.input_weight.set()
    ...


@rate_limit(5, 'set_name')
@dp.message_handler(Command('set_name'))
async def set_name(message: types.Message):
    if 1 < len(message.text) < 50:
        # TODO update name
        pass
    else:
        await message.answer('Имя должно быть от 1 до 50 символов')


@rate_limit(5, 'to_excel')
@dp.message_handler(Command('to_excel'))
async def to_excel(message: types.Message):
    await message.answer('Собираю данные...')
    workouts = []  # TODO получить все тренировки

    ...

    await message.answer_document(open(f'{message.from_user.id}.xlsx'), caption=f'Вот все твои тренировки')
