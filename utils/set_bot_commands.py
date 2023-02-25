from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Перезапуск бота'),
        types.BotCommand('help', 'Просмотр команд'),
        types.BotCommand('set_name', 'Сменить имя'),
        types.BotCommand('add_workout', 'Добавить тренировку'),
        types.BotCommand('calories', 'Норма калорий'),
        types.BotCommand('bmi', 'Индекс массы тела'),
        types.BotCommand('export', 'Получить свои тренировки'),
    ])
