# from aiogram.types import ReplyKeyboardRemove
# from aiogram.types import ReplyKeyboardMarkup
# from aiogram.types import KeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.types.message import Message


from models import User


numbers_to_emoji = {
        0: u'0️⃣',
        1: u'1️⃣',
        2: u'2️⃣',
        3: u'3️⃣',
        4: u'4️⃣',
        5: u'5️⃣',
        6: u'6️⃣',
        7: u'7️⃣',
        8: u'8️⃣',
        9: u'9️⃣',
    }
        

MINUS = u'➖'
PLUS = u'➕'


def i2e(num: int) -> str:
    if num < 0:
        result = MINUS
    else:
        result = ''

    digits = [d for d in str(abs(num))]
    for d in digits:
        result += numbers_to_emoji[int(d)]
    return result


def create_markup(user: User | None) -> InlineKeyboardMarkup:

    if not user:

        kb = InlineKeyboardMarkup()

        setup_increment_btn = InlineKeyboardButton('Setup increment', callback_data='setup increment')
        kb.add(setup_increment_btn)
        return kb

    elif user.current_level == 1:
        kb = InlineKeyboardMarkup(row_width=2)

        default_increment_btn = InlineKeyboardButton(
                f'Leave default {i2e(1)}', callback_data='setupdelta 1')

        delta_five_btn = InlineKeyboardButton(i2e(5), callback_data='setupdelta 5')
        delta_ten_btn = InlineKeyboardButton(i2e(10), callback_data='setupdelta 10')
        delta_fifteen_btn = InlineKeyboardButton(i2e(15), callback_data='setupdelta 15')


        kb.add(default_increment_btn)
        kb.row(delta_five_btn, delta_ten_btn, delta_fifteen_btn)
        return kb

    else:
        kb = InlineKeyboardMarkup()

        update_increment_btn = InlineKeyboardButton(
                'Update increment', callback_data='setup increment')


        minus_delta_button = InlineKeyboardButton(
                MINUS + i2e(user.delta), callback_data='minus')

        result_btn = InlineKeyboardButton(
                i2e(user.result), callback_data='something')

        plus_delta_button = InlineKeyboardButton(
                PLUS + i2e(user.delta), callback_data='plus')

        refresh_score = InlineKeyboardButton(
                f'Refresh score', callback_data='refresh_score')

        kb.add(update_increment_btn)
        kb.row(minus_delta_button, result_btn, plus_delta_button)
        kb.add(refresh_score)

    return kb
