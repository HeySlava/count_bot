about_message = """This bot will help you when you are doing monotonous counting.

The author uses this to count reps while exercising.

Known issues:

Feedback: @vyacheslav_kapitonov
"""


import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram.types import CallbackQuery
from aiogram.types.message import Message

import utils
from data import db_session
from data.state import State
from services import result_service
from services import user_service
from services.keyboard_service import UserKeyboard
from settings import settings


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=settings.token)
dp = Dispatcher(bot)


STATE_TO_MESSAGE = {
        State.WELCOME.value: 'Hello! Looks like you are new here',
        State.CHOOSE_INCREMENT.value: 'Choose increment for you',
        State.PROGRESS.value: 'Let\'s count it',
        State.CUSTOM_INCREMENT.value: 'Type increment for you. INTEGER'
        # State.CUSTOM_INCREMENT.value: 'You are choosing custom increment\nYou can abort it by pressing /restart'
    }


def setup_database():
    db_session.global_init(
            conn_str=settings.conn_str,
            debug=settings.debug,
        )


async def on_startup(dp):
    setup_database()

    await dp.bot.send_message(
            chat_id=settings.admin_id,
            text='Bot has started...',
        )


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

    text = f'Your score: {user.result}'
    await message.edit_text(text)
    await message.edit_reply_markup(reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'refresh_score')
async def refresh_score(callback_query: CallbackQuery):
    message = callback_query.message

    user = result_service.update_result(userid=message.chat.id)
    markup = UserKeyboard(user).markup

    await message.edit_text(STATE_TO_MESSAGE[user.current_state])
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


    user_service.update_user(
            userid=message.chat.id,
            delta=delta,
            state=state,
        )

    await message.answer(answer_message)


@dp.callback_query_handler(lambda _: True)
async def nothing(c: CallbackQuery):
    await c.answer()


if __name__ == '__main__':
    executor.start_polling(
            dp,
            on_startup=on_startup,
            relax=1,
        )
