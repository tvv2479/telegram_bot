# telegram_bot
Запросы в БД через телеграм-бот  
● добавить запись о продаже  
● получить данные о продажах за период 

Сгенерированная база для теста с **2023-01-01** по **2023-12-31**  

![db_bot](https://github.com/user-attachments/assets/6ae4f27c-5d2b-434b-8d31-dab465d85f2f)

**-** Запуск бота: bot.py   
**-** Работа с БД и подключение: папка dataa-base.py  
**-** Работа с сообщениями: admin_private.py  

На данный момент в боте отсутствуют проверки, отработки ошибок и неправильных вводов.  
Данные для проверки нужно вводить согласно вормата: 

● *user_id: числовой ввод*  
● *price: числовой ввод*  
● *first_date: ГГГГ-ММ-ДД*  
● *end_date: ГГГГ-ММ-ДД*

