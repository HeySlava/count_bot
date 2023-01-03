about_message = """This bot will help you when you are doing monotonous counting.

The author uses this to count reps while exercising.

Known issues:

Feedback: @vyacheslav_kapitonov
"""


import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor

from aiogram.types.message import Message
from aiogram.types import CallbackQuery

from pathlib import Path

import utils

from data.state import State
from data import db_session

from services import user_service
from services import result_service
from services.keyboard_service import UserKeyboard



API_TOKEN = '5707661701:AAHTMt4MqjYwpJCDoV-F-6eNoKY65R-omFA'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


STATE_TO_MESSAGE = {
        State.WELCOME.value: 'Hello! Looks like you are new here',
        State.CHOOSE_INCREMENT.value: 'Choose increment for you',
        State.PROGRESS.value: 'Let\'s count it',
        State.CUSTOM_INCREMENT.value: 'Type increment for you. INTEGER'
        # State.CUSTOM_INCREMENT.value: 'You are choosing custom increment\nYou can abort it by pressing /restart'
    }


def setup_database():
    DBDIR = Path('db')
    DBDIR.mkdir(exist_ok=True, parents=True)
    DBFILE = DBDIR / 'count.sqlite'
    CONN_STR = f'sqlite:///{DBFILE.as_posix()}'
    db_session.global_init(CONN_STR)


@dp.message_handler(commands=['about'])
async def about(message: Message):

    await message.answer(text=about_message)


@dp.message_handler(commands=['start'])
async def start(message: Message):

    user = user_service.get_user_by_userid(userid=message.chat.id)
    if not user:
        user = user_service.create_user(
                userid=message.chat.id,
                state=State.WELCOME)
        answer_message = STATE_TO_MESSAGE.get(user.current_state)

    if user.current_state == State.CUSTOM_INCREMENT.value:
        user = user_service.update_user(
                userid=message.chat.id,
                state=State.PROGRESS)

    markup = UserKeyboard(user).markup
    answer_message = STATE_TO_MESSAGE[user.current_state]

    await message.answer(text=answer_message, reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == str(State.CHOOSE_INCREMENT.value))
async def setup_increment(callback_query: CallbackQuery):
    message = callback_query.message

    user = user_service.update_user(
            userid=message.chat.id,
            state=State.CHOOSE_INCREMENT)
    markup = UserKeyboard(user).markup
    answer_message = STATE_TO_MESSAGE[user.current_state]

    await message.edit_text(text=answer_message)
    await message.edit_reply_markup(reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == str(State.CUSTOM_INCREMENT.value))
async def custom_increment(callback_query: CallbackQuery):
    message = callback_query.message

    user = user_service.update_user(
            userid=message.chat.id,
            state=State.CUSTOM_INCREMENT)

    markup = UserKeyboard(user).markup
    answer_message = STATE_TO_MESSAGE[user.current_state]

    await message.edit_text(text=answer_message)
    await message.edit_reply_markup(reply_markup=markup)


@dp.callback_query_handler(lambda c: 'setupdelta' in c.data)
async def change_increment(callback_query: CallbackQuery):
    message = callback_query.message

    delta = int(callback_query.data.split()[-1])

    user = user_service.update_user(
            userid=message.chat.id,
            delta=delta,
            state=State.PROGRESS)
    markup = UserKeyboard(user).markup
    answer_message = STATE_TO_MESSAGE[user.current_state]

    await message.edit_text(text=answer_message)
    await message.edit_reply_markup(reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data in ('plus', 'minus'))
async def countit(callback_query: CallbackQuery):
    message = callback_query.message

    user = result_service.update_result(
            userid=message.chat.id,
            mode=callback_query.data)
    markup = UserKeyboard(user).markup

    await message.edit_reply_markup(reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'refresh_score')
async def refresh_score(callback_query: CallbackQuery):
    message = callback_query.message

    user = result_service.update_result(userid=message.chat.id)
    markup = UserKeyboard(user).markup

    await message.edit_reply_markup(reply_markup=markup)


@dp.message_handler(lambda message: user_service.get_user_by_userid(userid=message.chat.id).current_state == State.CUSTOM_INCREMENT.value)
async def setup_value_custom_increment(message: Message):

    delta = utils.try_int(message.text)

    if not delta:
        answer_message = 'Increment must by INTEGER.\nFor instance 42'
        state = State.CUSTOM_INCREMENT
    else:
        answer_message = 'Success! Now, you can refresh your keyboard or turn it back /start'
        state = State.PROGRESS


    _ = user_service.update_user(
            userid=message.chat.id,
            delta=delta,
            state=state)

    await message.answer(answer_message)


@dp.callback_query_handler(lambda _: True)
async def nothing(callback_query: CallbackQuery):
    message = callback_query.message

    user = user_service.update_user(
            userid=message.chat.id,
            state=State.PROGRESS)
    markup = UserKeyboard(user).markup
    answer_message = STATE_TO_MESSAGE[user.current_state]

    await message.edit_text(text=answer_message)
    await message.edit_reply_markup(reply_markup=markup)

if __name__ == '__main__':
    setup_database()
    executor.start_polling(dp)
