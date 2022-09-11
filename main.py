import logging

from aiogram.types import CallbackQuery

import database
import keyboard as kb

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram.types.message import Message

API_TOKEN = '5737951316:AAET6k4aHsZ2oe9_1MtI1WiwcUY6kKXBn7U'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: Message):

    user = database.get_user_by_userid(userid=message.chat.id)
    markup = kb.create_markup(user=user)

    await message.answer(text='Base setup', reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'default')
async def default(callback_query: CallbackQuery):
    message = callback_query.message 

    user = database.create_user(userid=message.chat.id, delta=1)
    markup = kb.create_markup(user=user)

    await message.answer(text="Let's count it", reply_markup=markup)


@dp.message_handler(regexp=r'\/setupdelta')
async def setupdelta(message: Message):

    try:
        change_delta = int(message.text.split()[-1])
    except ValueError:
        await message.answer('Usage for setup: /setup INTEGER')
    else:
        user = database.create_user(userid=message.chat.id, delta=change_delta)
        markup = kb.create_markup(user=user)

        await message.answer(text="Let's count it", reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'plus')
async def plus(callback_query: CallbackQuery):
    message = callback_query.message

    user = database.change_result(userid=message.chat.id, mode='plus')

    markup = kb.create_markup(user=user)

    await message.edit_reply_markup(reply_markup=markup)



@dp.callback_query_handler(lambda c: c.data == 'refresh_score')
async def refresh_score(callback_query: CallbackQuery):
    message = callback_query.message

    user = database.refresh_score(userid=message.chat.id)

    markup = kb.create_markup(user=user)

    await message.edit_reply_markup(reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'minus')
async def minus(callback_query: CallbackQuery):
    message = callback_query.message

    user = database.change_result(userid=message.chat.id, mode='minus')

    markup = kb.create_markup(user=user)

    await message.edit_reply_markup(reply_markup=markup)


if __name__ == '__main__':
    executor.start_polling(dp)
