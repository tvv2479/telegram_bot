
# Команды для меню бота

from aiogram.types import BotCommand


private = [
    BotCommand(command='insert', description='Добавить продажу'),
    BotCommand(command='select', description='Получить отчет')
]