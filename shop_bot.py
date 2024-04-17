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



from aiogram import Bot, Dispatcher, types, F
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
existing_orders_markup = None 

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
    orders_info_list = []
    for order in reversed(orders):
        order_info = f"Заказ {order.id}:\n" \
                     f"Дата создания: {order.created_at}\n" \
                     f"Дата обновления: {order.updated_at}\n" \
                     f"Общая цена: {order.total_price}\n" \
                     f"Статус: {order.get_status_display()}\n\n"
        orders_info_list.append(order_info)
    return orders_info_list







# def send_telegram_notification(old_status, new_status, username):
#     status = (f"Статус заказа изменён: {old_status} -> {new_status}. Пользователь: {username}")
    
    
    

mainmenu = InlineKeyboardBuilder()
mainmenu.row(types.InlineKeyboardButton(text="Ваші замовлення", callback_data="us_orders"))
        
        
        
def gen_button_orders_list(num_order, orders):
    markup = InlineKeyboardBuilder()
    # Получаем количество заказов
    length_orders = len(orders)
    if num_order == 0:
        markup.row(
            types.InlineKeyboardButton(text="⏭️Наступний", callback_data=f"orders_list_{num_order+1}")
        )
    elif num_order == length_orders - 1:
        markup.row(
            types.InlineKeyboardButton(text="⏮️Назад", callback_data=f"orders_list_{num_order-1}"),
            types.InlineKeyboardButton(text=f"{num_order+1}/{length_orders}", callback_data="none"),
            types.InlineKeyboardButton(text="🔚Кінець", callback_data=f"orders_list_0")
        )
    else:
        markup.row(
            types.InlineKeyboardButton(text="⏮️Назад", callback_data=f"orders_list_{num_order-1}"),
            types.InlineKeyboardButton(text=f"{num_order+1}/{length_orders}", callback_data="none"),
            types.InlineKeyboardButton(text="⏭️Наступний", callback_data=f"orders_list_{num_order+1}")
        )
    return markup





        
        

@dp.message(Command('orders'))
async def get_user_orders(message: types.Message, state: FSMContext):
    try:
        user = await check_user(message.from_user.username)
        data_us = user["database_username"]
        
        orders_info_list = await sync_to_async(fetch_orders)(data_us)
        if not orders_info_list:
            await message.answer("В вас нема замовлень")
            return
        elif len(orders_info_list) <= 3:
            await message.answer("\n\n".join(orders_info_list))
            return

        current_order_index = 0
        current_order_info = orders_info_list[current_order_index]

        markup = gen_button_orders_list(current_order_index, orders_info_list)
        await message.answer(current_order_info, reply_markup=markup.as_markup())

        # Сохраняем информацию о текущем заказе в контексте, чтобы использовать её при перелистывании
        await state.update_data(orders_info_list=orders_info_list, current_order_index=current_order_index)

    except Exception as e:
        print(f"помилка: {e}")


@dp.callback_query(F.data.startswith("orders_list_"))
async def next_order(call: types.CallbackQuery, state: FSMContext):
    call.message.delete_reply_markup()
    user = await check_user(call.from_user.username)
    data_us = user["database_username"]
    orders_info_list = await sync_to_async(fetch_orders)(data_us)
    
    num_order = int(call.data.split("_")[-1])
    try:
        order_info = orders_info_list[num_order]
    except IndexError:
        call.message.answer("Такого заказа не існує")
        try:
            await call.message.delete()
        except:
            pass

    markup = gen_button_orders_list(num_order, orders_info_list)
    await call.message.answer(order_info, reply_markup=markup.as_markup())

    try:
        await call.message.delete()
    except:
        pass
        
        
        
        
        
async def main() -> None:
    bot = Bot(API_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())