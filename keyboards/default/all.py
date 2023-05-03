from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel = ReplyKeyboardMarkup([
    [KeyboardButton(text='Отмена ❌')]
])

genders = ReplyKeyboardMarkup([
    [KeyboardButton(text='Мужской 🕺🏻'), KeyboardButton(text='Женский 💃🏼')]
])

activity_degrees = ReplyKeyboardMarkup([
    [KeyboardButton(text='Сидячий образ жизни без нагрузок 🛋️')],
    [KeyboardButton(text='Тренировки  1-3 раза в неделю 🥉')],
    [KeyboardButton(text='Занятия 3-5 дней в неделю 🥈')],
    [KeyboardButton(text='Интенсивные тренировки 6-7 раз в неделю 🥇')],
    [KeyboardButton(text='Упражнения чаще, чем раз в день 🏆')],
])
