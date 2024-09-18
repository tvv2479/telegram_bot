
# Создание случайного датасета для таблийы

import pandas as pd
import random
import datetime

# СЛУЧАЙНЫЙ НАБОР ДАННЫХ

def datas():
    # Генерация диапазона дат 1 год
    dateList = ([datetime.datetime.strptime("2023-12-31", "%Y-%m-%d").date()
                - datetime.timedelta(days=x)
                for x in range(365)])

    # Генерация цен
    priceList = [x for x in range(8500, 538453)]

    # генерация user_id
    userList = [x for x in range(2853, 5383)]

    # Генерация заказов
    ordersList =  [x for x in range(98423, 104285)]

    # Формирование строк датафрейма
    dfInsert = []
    for ord in ordersList:
        dat = []
        dat.append(ord)
        dat.append(random.choice(userList))
        dat.append(random.choice(dateList))
        dat.append(random.choice(priceList))
        
        dfInsert.append(dat)

    # Создание датафрейма
    df = pd.DataFrame(dfInsert,
                    columns=['order_id', 'user_id', 'date_insert', 'price']
                    )

    return df[['user_id', 'date_insert', 'price']]



