import asyncio
import logging
import os
import sys

from PIL import Image
from decouple import config
import django
import json

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hbold
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from asgiref.sync import sync_to_async
from django.contrib.auth.hashers import make_password, check_password


API_TOKEN = config('API_TOKEN')
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()


from django.contrib.auth.models import User


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
        'user_is_logging': True,
        'is_main':True,
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
    
    
   
   
    
    
# def check_user(from_user: types.User):
#     user_id = from_user.id
#     for user in users:
#         if user['id'] == user_id:
#             return user
#     return (user_id, from_user.username, from_user.full_name)



async def check_user(users_info, id):
    for user in users_info:
        if user["id"] == id:
            return user

@dp.message(Command("orders"))
async def orders(message: types.Message):
    info_about_user = await read_users_from_file()
    is_user = await check_user(info_about_user, message.from_user.username)
    if is_user:
        print(is_user["database_username"])
    else:
        print("User not found")





async def main() -> None:
    bot = Bot(API_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())