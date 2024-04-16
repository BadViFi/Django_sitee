import os
import sys
import asyncio
import logging

# Установка переменной окружения до импорта Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()

from decouple import config
from PIL import Image
import json
import threading

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hbold
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import bold
from asgiref.sync import sync_to_async
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from apps.order.models import Order

API_TOKEN = config('API_TOKEN')
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


class RegisterState(StatesGroup):
    say_username = State()
    say_password = State()
    say_tg_username = State()


@dp.message(Command("login"))
async def username(message: types.Message, state: FSMContext):
    await state.set_state(RegisterState.say_username)
    await message.answer("надішліть ваш юзернейм")
    
    
    
@dp.message(RegisterState.say_username)
async def password(message: types.Message, state: FSMContext):
    try:
        say_username = str(message.text)
        await state.update_data(say_username = say_username)
        print(say_username)
        await state.set_state(RegisterState.say_password)
        await message.answer("надішліть ваш пароль")
    except:
        await message.answer("сталася помилкаaaaa")
    
    
@dp.message(RegisterState.say_password)
async def login(message: types.Message, state: FSMContext):
    say_password = str(message.text)
    data = await state.get_data()
    say_username = data.get('say_username')
    

    queryset = await sync_to_async(User.objects.filter)(username=say_username)
    user = await sync_to_async(queryset.first)()
    

    if not user or not check_password(say_password, user.password):
        await message.answer("такого користувача не знайдено")
        await state.clear()
        return

    user_data = {
        'id': message.from_user.username,
        'database_username': user.username,
        'password': make_password(say_password),
        'user_is_logging': True
    }

    users = await read_users_from_file()
    



    existing_user = next((u for u in users if u.get('database_username') == user.username), None)
    if existing_user and existing_user.get('id') == message.from_user.username:
        await message.answer("такий користувач вже знайден")
        await state.clear()
        return
    
    for uniq in users:
        if uniq["id"] == message.from_user.username:
            await message.answer(f"Користувач з таким юзернеймом в телеграмі вже існує, вам потрібно вийти з аккаунту щоб перейти на інший")
            await state.clear()
            return

        
    users.append(user_data)

    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

    await message.answer(f"ви успішно увійшли як {user.username}")
    await state.clear()



    
        


async def read_users_from_file():
    try:
        with open('users.json', 'r') as f:
            users_info = json.load(f)
            return users_info
        
    except FileNotFoundError:
        return []
    
    
   
@dp.message(Command("logout"))
async def delete_user_from_file(message: types.Message) -> None:
    try:
        
        users_info = await read_users_from_file()

        updated_users = [user for user in users_info if user['id'] != message.from_user.username]


        with open('users.json', 'w') as f:
            json.dump(updated_users, f, indent=4)
        await message.answer("ви успішно вийшли з аккаунту")
        
    except FileNotFoundError:
        print("Файл не знайдений")

    
    



async def check_user(id):
    users_info = await read_users_from_file()
    for user in users_info:
        if user["id"] == id:
            return user





def fetch_orders(data_us):
    orders = Order.objects.filter(user__username=data_us)
    orders_info = ""
    for order in orders:
        orders_info += f"Заказ {order.id}:\n" \
                       f"Дата создания: {order.created_at}\n" \
                       f"Дата обновления: {order.updated_at}\n" \
                       f"Общая цена: {order.total_price}\n" \
                       f"Статус: {order.get_status_display()}\n\n"
    return orders_info

@dp.message(Command('orders'))
async def get_user_orders(message: types.Message):
    try:
        user = await check_user(message.from_user.username)
        data_us = user["database_username"]
        
        orders_info = await sync_to_async(fetch_orders)(data_us)
        
        await message.answer(orders_info)
        
    except Exception as e:
        print(f"помилка: {e}")



def send_telegram_notification(old_status, new_status, username):
    chat_id = 1031341752 
    status = (f"Статус заказа изменён: {old_status} -> {new_status}. Пользователь: {username}")
    
    



# async def get_user_orders(message: types.Message):
#     chat_id = 1031341752 
#     status = await sync_to_async(send_telegram_notification)
#     bot.send_message(chat_id=chat_id, text=message)
#     print(status)
    




async def main() -> None:
    bot = Bot(API_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())