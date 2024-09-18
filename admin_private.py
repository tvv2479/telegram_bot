'''
Административный функционал для доступа и взаимодействия с БД
'''

from datetime import datetime

from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from data_base.engine_bd import insertRow, report, check
from chat_types import ChatTypeFilter


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]))

# Функция для быстрого формирования кнопок
def get_keyboard(
    *btns: str,
    placeholder: str = None,
    request_contact: int = None,
    request_location: int = None,
    sizes: tuple[int] = (2,1),
):
    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):
        
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))

        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
            resize_keyboard=True, input_field_placeholder=placeholder)

# Надписи кнопок
ADMIN_KB = get_keyboard(
    "Добавить продажу",
    "Получить отчет",
    placeholder="Выберите действие",
    sizes=(2,1),
)


@admin_router.message(Command("start"))
async def admin_features(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)
    

# Код ниже для машины состояний (FSM)

# КНОПКА "ДОБАВИТЬ ПРОДАЖУ"
class AddSale(StatesGroup):
    # Шаги состояний
    user_id = State()
    price = State()
    
# Становимся в состояние ожидания ввода user_id
@admin_router.message(StateFilter(None), or_f(Command('insert'), F.text == "Добавить продажу"))
async def add_sale(message: types.Message, state: FSMContext):
    await message.answer("Введите user_id:", 
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddSale.user_id) # Ожидание ввода user_id от пользователя
    
# Ловим данные для состояние user_id и потом меняем состояние на price
@admin_router.message(AddSale.user_id, F.text)
async def add_user_id(message: types.Message, state: FSMContext):
    # Здесь можно сделать какую либо дополнительную проверку
    # Выходим из хендлера не меняя состояние с отправкой сообщения
    # if len(message.text) < 1:
    #     await message.answer("Значение не может быть пустым. \n Введите заново")
    #     return
    
    await state.update_data(user_id=message.text) # Сохранения полученных от пользователя данные
    await message.answer("Введите цену заказа в формате 000.00:") # Ответное сообщение пользователю
    await state.set_state(AddSale.price) # Ожидание ввода price от пользователя
    
#Ловим данные для состояние price и потом сохраняем все полученные данные от пользователя
@admin_router.message(AddSale.price, F.text)
async def add_price(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(price=message.text) # Сохранения полученных от пользователя данные
    await message.answer("Продажа добавлена", reply_markup=ADMIN_KB)
    data = await state.get_data() # Сохранение полученных данных
    # await message.answer(str(data)) # Преобразовать данные в строку и отправить в чат для проверки
    # Записываем данные в базу
    insertRow(data['user_id'], float(data['price']))
    # Сохранить изменения сессии
    await session.commit()
    await message.answer(check())
    await state.clear() # Очистка состояний пользователея и очистка данных. Данные уже в переменной.

# # Хендлер для отлова некорректных ввода для состояния price
# @admin_router.message(AddSale.price)
# async def add_price2(message: types.Message, state: FSMContext):
#     await message.answer("Вы ввели не допустимые данные, введите стоимость товара")


# КНОПКА "ПОЛУЧИТЬ ОТЧЕТ"
class GetReport(StatesGroup):
    # Шаги состояний
    first_date = State()
    end_date = State()
    
# Становимся в состояние ожидания ввода first_date
@admin_router.message(StateFilter(None), or_f(Command('select'), F.text == "Получить отчет"))
async def get_report(message: types.Message, state: FSMContext):
    await message.answer("Введите начальную дату периода в формате ГГГГ-ММ-ДД:", 
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(GetReport.first_date) # Ожидание ввода начальной даты периода от пользователя

# Ловим данные для состояние first_date и потом меняем состояние на end_date
@admin_router.message(GetReport.first_date, F.text)
async def get_first_date(message: types.Message, state: FSMContext):    
    await state.update_data(first_date=message.text) # Сохранения полученных от пользователя данные
    await message.answer("Введите крайнюю дату периода в формате ГГГГ-ММ-ДД:") # Ответное сообщение пользователю
    await state.set_state(GetReport.end_date) # Ожидание ввода крайней даты периода от пользователя

#Ловим данные для состояние end_date и потом сохраняем все полученные данные от пользователя
@admin_router.message(GetReport.end_date, F.text)
async def get_end_date(message: types.Message, state: FSMContext):    
    await state.update_data(end_date=message.text) # Сохранения полученных от пользователя данные
    await message.answer("Период сформирован", reply_markup=ADMIN_KB)
    data_rep = await state.get_data() # Сохранение полученных данных
    await message.answer(report(data_rep['first_date'], data_rep['end_date'])) # Отправить вывод в чат
    await state.clear() # Очистка состояний пользователея и очистка данных. Данные уже в переменной.

