import asyncio
import datetime as dt
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram.types import BotCommand
from aiogram.types import CallbackQuery
from aiogram.types.message import Message

import utils
from data import db_session
from data.state import State
from filters import check_user_custom_increment
from filters import filter_by_state
from filters import is_user_stored_before
from kb import init_user_keyboard
from services import result_service
from services import user_service
from settings import settings
from static.messages import ABOUT_MESSAGE


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=settings.token)
dp = Dispatcher(bot)


STATE_TO_MESSAGE = {
        State.WELCOME.value: 'Hello! Looks like you are new here',
        State.CHOOSE_INCREMENT.value: 'Choose an increment for yourself',
        State.PROGRESS.value: 'Let\'s count it',
        State.CUSTOM_INCREMENT.value: (
            'Choose an increment for '
            'yourself. INTEGER'
        )
    }


@dp.message_handler(lambda m: not is_user_stored_before(m.from_user.id))
async def handle_new_user(message: Message):
    user = user_service.create_user(
            userid=message.from_user.id,
            state=State.WELCOME,
        )
    answer_message = STATE_TO_MESSAGE[user.current_state]
    kb = init_user_keyboard(user)
    await message.answer(text=answer_message, reply_markup=kb.create_markup())


@dp.message_handler(commands=['start'])
async def start(message: Message):
    user = user_service.get_user_by_userid(userid=message.from_user.id)

    user = user_service.update_user(
            userid=message.from_user.id,
            state=State.PROGRESS,
        )

    answer_message = STATE_TO_MESSAGE[user.current_state]
    kb = init_user_keyboard(user)
    await message.answer(text=answer_message, reply_markup=kb.create_markup())


@dp.message_handler(commands=['about'])
async def about(message: Message):
    await message.answer(text=ABOUT_MESSAGE)


@dp.callback_query_handler(
        lambda c: c.data == str(State.CHOOSE_INCREMENT.value)
    )
async def setup_increment(callback_query: CallbackQuery):
    message = callback_query.message

    user = user_service.update_user(
            userid=message.chat.id,
            state=State.CHOOSE_INCREMENT)

    answer_message = STATE_TO_MESSAGE[user.current_state]

    kb = init_user_keyboard(user)
    await message.edit_text(text=answer_message)
    await message.edit_reply_markup(reply_markup=kb.create_markup())


@dp.callback_query_handler(
        lambda c: c.data == str(State.CUSTOM_INCREMENT.value)
    )
async def custom_increment(callback_query: CallbackQuery):
    message = callback_query.message

    user = user_service.update_user(
            userid=message.chat.id,
            state=State.CUSTOM_INCREMENT)

    kb = init_user_keyboard(user)
    answer_message = STATE_TO_MESSAGE[user.current_state]

    await message.edit_reply_markup(reply_markup=kb.create_markup())
    await message.answer(text=answer_message)
    await callback_query.answer()


@dp.callback_query_handler(lambda c: 'setupdelta' in c.data)
async def change_increment(callback_query: CallbackQuery):
    message = callback_query.message

    delta = int(callback_query.data.split()[-1])

    user = user_service.update_user(
            userid=message.chat.id,
            delta=delta,
            state=State.PROGRESS)
    kb = init_user_keyboard(user)
    answer_message = STATE_TO_MESSAGE[user.current_state]

    await message.edit_text(text=answer_message)
    await message.edit_reply_markup(reply_markup=kb.create_markup())


@dp.callback_query_handler(lambda c: c.data in ('plus', 'minus'))
async def countit(callback_query: CallbackQuery):
    message = callback_query.message

    user = result_service.update_result(
            userid=message.chat.id,
            mode=callback_query.data)
    kb = init_user_keyboard(user)

    utcnow = dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    text = (
            f'Your score: {user.result!r}\n'
            f'UTC time: {utcnow}'
        )
    await message.edit_text(text)
    await message.edit_reply_markup(reply_markup=kb.create_markup())


@dp.callback_query_handler(lambda c: c.data == 'refresh_score')
async def refresh_score(callback_query: CallbackQuery):
    message = callback_query.message

    user = result_service.update_result(userid=message.chat.id)
    kb = init_user_keyboard(user)

    await message.edit_text(STATE_TO_MESSAGE[user.current_state])
    await message.edit_reply_markup(reply_markup=kb.create_markup())


@dp.message_handler(
        lambda m: check_user_custom_increment(m.text),
        lambda m: filter_by_state(
            m.from_user.id,
            State.CUSTOM_INCREMENT,
        ),
    )
async def setup_value_custom_increment(message: Message):
    delta = utils.try_positive_int(message.text)
    user_service.update_user(
            userid=message.chat.id,
            delta=delta,
            state=State.PROGRESS,
        )

    answer_message = (
            'Success! Now, you can refresh your keyboard '
            'or turn it back /start'
        )
    await message.answer(answer_message)


@dp.message_handler(
        lambda m: filter_by_state(
            m.from_user.id,
            State.CUSTOM_INCREMENT,
        )
    )
async def wrong_user_input(message: Message):
    answer_message = (
            'Increment must by positive INTEGER.\n'
            'For instance 42'
        )
    await message.answer(answer_message)


@dp.message_handler(lambda _: True)
async def any(m: Message):
    answer = (
            "You aren't using this bot correctly. Try again\n"
            '/start'
            '\n'
            '\n'
            'Your message will be deleted in 10 seconds'
        )
    response_message = await m.reply(answer)
    await asyncio.sleep(10)
    await bot.delete_message(chat_id=m.chat.id, message_id=m.message_id)
    await bot.delete_message(
            chat_id=response_message.chat.id,
            message_id=response_message.message_id,
        )


@dp.callback_query_handler(lambda _: True)
async def nothing(c: CallbackQuery):
    await c.answer()


async def set_commands(bot) -> None:
    commands = [
        BotCommand(command='/start', description='Start right now'),
        BotCommand(command='/about', description='Motivation to use it')
    ]
    await bot.set_my_commands(commands)


async def send_startup_message(bot) -> None:
    await bot.send_message(
            chat_id=settings.admin_id,
            text='Bot has started...',
        )


def setup_database():
    db_session.global_init(
            conn_str=settings.conn_str,
            debug=settings.debug,
        )


async def on_startup(dp):
    setup_database()
    await set_commands(dp.bot)
    await send_startup_message(dp.bot)


if __name__ == '__main__':
    executor.start_polling(
            dp,
            on_startup=on_startup,
            relax=1,
        )
