# Коннект с БД. Создание и удаление таблиц
# Асинхроное подключение

import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import configparser

from data_base.models import Base


config = configparser.ConfigParser()
config.read("E:/Projects/komandor/config.ini")

# Подключение к базе аналитики
BdAnalisHost = config['KeyBd']['host']
BdAnalisUser = config['KeyBd']['bd_user']
BdAnalisName = config['KeyBd']['bd_name']
BdAnalisPass = config['KeyBd']['password']

DB_URL = config['DbAsinc']['DB_URL']

#engine = create_engine(f'postgresql+psycopg2://{BdAnalisUser}:{BdAnalisPass}@{BdAnalisHost}/{BdAnalisName}')

engine = create_async_engine(DB_URL, echo=True)

# Сессии для запросов в БД
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)