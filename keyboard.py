# from aiogram.types import ReplyKeyboardRemove
# from aiogram.types import ReplyKeyboardMarkup
# from aiogram.types import KeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.types.message import Message

from models import User


def create_markup(user: User | None) -> InlineKeyboardMarkup:

    if not user:
        kb = InlineKeyboardMarkup()
        change_delta_btn = InlineKeyboardButton(
                'Setup custom delta\n'\
                'Must be INTEGER', switch_inline_query_current_chat='/setupdelta ')
        default_delta_btn = InlineKeyboardButton('Leave as +1 and -1', callback_data='default')

        kb.add(change_delta_btn).add(default_delta_btn)

    else:
        kb = InlineKeyboardMarkup()
        minus_delta_button = InlineKeyboardButton(
                f'Minus {user.delta}', callback_data='minus')

        result_btn = InlineKeyboardButton(
                f'Score {user.result}', callback_data='something')

        plus_delta_button = InlineKeyboardButton(
                f'Plus {user.delta}', callback_data='plus')

        refresh_score = InlineKeyboardButton(
                f'Refresh score', callback_data='refresh_score')

        kb.row(minus_delta_button, result_btn, plus_delta_button)
        kb.add(refresh_score)

    return kb
