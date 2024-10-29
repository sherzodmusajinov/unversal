


from urllib.request import urlretrieve
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

api_key = 'aOSWs3U5QvhE3JZjhalCpw==YVhXPds6cQpza1bc'
API_TOKEN = '7895589628:AAFmobg7FhKOBpuN_CoXYjqjECX90uy09jw'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    waiting_for_length = State()  # Parol uzunligini kutish
    waiting_for_logo_name = State()  # Logotip nomini kutish
    waiting_for_price_name = State()

def main_key():
    buttons = InlineKeyboardMarkup()
    buttons.add(InlineKeyboardButton("Logo", callback_data='logo'))
    buttons.add(InlineKeyboardButton("Password Generator", callback_data='length'))
    buttons.add(InlineKeyboardButton("Commodity Price", callback_data='price'))
    return buttons


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Assalomu aleykum! Quydagilardan birini tanlang:", reply_markup=main_key())


@dp.callback_query_handler(lambda c: c.data == 'length')
async def password_button_handler(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,
                           "Random parolar olish uchun\nKod necha xonali bolishini kiriting:")
    await UserState.waiting_for_length.set()


@dp.message_handler(state=UserState.waiting_for_length)
async def get_password(message: types.Message, state: FSMContext):
    length = message.text
    api_url = f'https://api.api-ninjas.com/v1/passwordgenerator?length={length}'
    response = requests.get(api_url, headers={'X-Api-Key': api_key})

    if response.status_code == requests.codes.ok:
        await bot.send_message(message.from_user.id, response.text)
    else:
        await bot.send_message(message.from_user.id, "Xatolik yuz berdi: {}".format(response.text))

    await UserState.next()


@dp.callback_query_handler(lambda c: c.data == 'logo')
async def logo_button_handler(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Logotip uchun nomni kiriting:")
    await UserState.waiting_for_logo_name.set()


@dp.message_handler(state=UserState.waiting_for_logo_name)
async def get_logo(message: types.Message, state: FSMContext):
    logo_name = message.text
    api_url = f'https://api.api-ninjas.com/v1/logo?name={logo_name}'
    response = requests.get(api_url, headers={'X-Api-Key': api_key})

    if response.status_code == requests.codes.ok:
        await bot.send_message(message.from_user.id, response.text)
    else:
        await bot.send_message(message.from_user.id, "Xatolik yuz berdi: {}".format(response.text))

    await UserState.next()  # Holatni tugatamiz
@dp.callback_query_handler(lambda c: c.data == 'price')
async def price_button_handler(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Tavarni narxini etadi:")
    await UserState.waiting_for_logo_name.set()


@dp.message_handler(state=UserState.waiting_for_price_name)
async def get_prece(message: types.Message, state: FSMContext):
    many = message.text
    api_url = 'https://api.api-ninjas.com/v1/commodityprice?name={}'.format(many)
    response = requests.get(api_url, headers={'X-Api-Key': api_key})

    if response.status_code == requests.codes.ok:
        await bot.send_message(message.from_user.id, response.text)
    else:
        await bot.send_message(message.from_user.id, "Xatolik yuz berdi: {}".format(response.text))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
