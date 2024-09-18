
'''
Подключение к базе данных и работа с таблицами.\n
Функции:\n
readBd - Чтение из БД по sql запросу;\n
insertDataset - Добавление данных в таблицу из DataFrame;\n
insertRow - Добавление строки данных.
'''


from sqlalchemy import text, table, column
from sqlalchemy import create_engine
from sqlalchemy import insert, select
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import configparser
import psycopg2

config = configparser.ConfigParser()
config.read("E:/Projects/komandor/config.ini")

# Подключение к базе аналитики
BdAnalisHost = config['KeyBd']['host']
BdAnalisUser = config['KeyBd']['bd_user']
BdAnalisName = config['KeyBd']['bd_name']
BdAnalisPass = config['KeyBd']['password']

engine = create_engine(f'postgresql+psycopg2://{BdAnalisUser}:{BdAnalisPass}@{BdAnalisHost}/{BdAnalisName}')

# Объявление объекта таблицы для sqlalchemy ORM
test_tele = table("test_tele",
            column("order_id"),
            column("user_id"),
            column("date_insert"),
            column("price")
            )   


# Чтение файла csv

def readBd(sql):
    '''
    Функция выводит данные по запросу SQL.\n
    '''
    return pd.read_sql(sql, engine)

# Добавление датасета в базу
def insertDataset(dataset, table):
    '''
    Функция загружает данные в таблицу.\n
    dataset - набор данных\n
    table - наименование таблицы
    '''
    dataset.to_sql(f'{table}', 
                   engine, 
                   schema='public', 
                   if_exists='append', 
                   index=False)
    

# Вставка записи в базу test_tele

def insertRow(user_id=None, price=None):
    '''
    Функция добавляет одну строку в базу test_tele.\n
    Значения oeder_id и date_insert заполняются автоматически.\n
    Пользовательский ввод:\n
    user_id - по умолчанию None\n
    table - по умолчанию None
    '''
    with engine.connect() as conn:
        conn.execute(insert(test_tele),
                     [
                         {'user_id': user_id,
                          'date_insert':datetime.today().date().strftime('%Y-%m-%d'),
                          'price': price}
                     ])
        conn.commit()

# Отчет за период

def report(start_date, end_date):
    sql = f'''select * 
               from test_tele
              where date_insert between '{start_date}' and '{end_date}'
              order by date_insert asc'''

    df25 = pd.read_sql(sql, engine)
    
    return f'''
            Отчет по данным за выбранный период:\n
            Количествово покупателей - {df25['user_id'].nunique()} человек.\n
            Количество заказов - {df25['order_id'].nunique()} штук.\n
            Выручка за период - {sum(list(df25['price']))} руб.\n
            Выручка на одного клиента - {round(sum(list(df25['price'])) / df25['user_id'].nunique(), 2)} руб.\n
            Средний чек - {df25['price'].median()} руб.
            '''



# Проверка записи в базу
def check():
    sql = '''select * 
               from test_tele
              order by order_id desc 
              limit 1'''
    
    df = pd.read_sql(sql, engine)
    d = df.to_numpy()
    orders = d[0][0]
    users = d[0][1]
    dat = d[0][2].strftime('%Y-%m-%d')
    price = d[0][3]
    return f'''
            Вот ваша запись о продаже:\n
            Заказ №: {orders};\n
            Клиент №: {users};\n
            Дата: {dat};\n
            Сумма руб.: {price}
            '''


