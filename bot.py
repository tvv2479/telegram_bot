

import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

import configparser

#from bot_support.user_ptivate import user_private_router
from admin_private import admin_router
from bot_cmd_list import private
from data_base.engine import session_maker
from data_base.db import DataBaseSession


config = configparser.ConfigParser()
config.read("E:/Projects/komandor/config.ini")

TOKEN = config['BotTel']['token']

bot = Bot(token=TOKEN)
# bot.my_admins_list = [] # Список юзеров, оторые могут добавлять сделки и получать отчеты

# Класс отвечает за фильтрацию сообщений, которые получает бот от сервера Телеграм
dp = Dispatcher()
# dp.include_routers(user_private_router)
dp.include_router(admin_router)



# Постоянная прослушка ботом сервера Телеграм о наличии изменений для бота 
async def main():
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await bot.delete_webhook(drop_pending_updates=True) # Пропустить ожидающие обновления если бот был offline
    #await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats()) # Если нужно удалить команды из меню бота
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats()) # type: ignore
    await dp.start_polling(bot, allowed_updates=['massage', 'edited_massege'])

asyncio.run(main())



