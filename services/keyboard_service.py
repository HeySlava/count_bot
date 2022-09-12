from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


from data.user import User
from data.state import State
from utils import i2e, PLUS, MINUS


class UserKeyboard:

    def __init__(self, user: User):
        self.user = user
        self._kb = InlineKeyboardMarkup()

    @property
    def markup(self):
        return self._create_markup()

    def _create_markup(self):
        if self.user.current_state == State.WELCOME.value:
            return self._welcome_markup()

        if self.user.current_state == State.CHOOSE_INCREMENT.value:
            return self._choose_increment_markup()

        if self.user.current_state == State.PROGRESS.value:
            return self._progress_markup()

    def _welcome_markup(self):

        setup_increment_btn = InlineKeyboardButton(
                'Setup increment', callback_data=str(State.CHOOSE_INCREMENT.value))

        self._kb.add(setup_increment_btn)
        return self._kb


    def _choose_increment_markup(self):
            default_increment_btn = InlineKeyboardButton(
                    f'Leave default {i2e(1)}', callback_data='setupdelta 1')

            delta_five_btn = InlineKeyboardButton(i2e(5), callback_data='setupdelta 5')
            delta_ten_btn = InlineKeyboardButton(i2e(10), callback_data='setupdelta 10')
            delta_fifteen_btn = InlineKeyboardButton(i2e(15), callback_data='setupdelta 15')

            self._kb.add(default_increment_btn)
            self._kb.row(delta_five_btn, delta_ten_btn, delta_fifteen_btn)
            return self._kb


    def _progress_markup(self):

        update_increment_btn = InlineKeyboardButton(
                'Change increment', callback_data=str(State.CHOOSE_INCREMENT.value))

        minus_delta_button = InlineKeyboardButton(
                MINUS + i2e(self.user.delta), callback_data='minus')

        result_btn = InlineKeyboardButton(
                i2e(self.user.result), callback_data='something')

        plus_delta_button = InlineKeyboardButton(
                PLUS + i2e(self.user.delta), callback_data='plus')

        refresh_score = InlineKeyboardButton(
                f'Refresh score', callback_data='refresh_score')

        self._kb.add(update_increment_btn)
        self._kb.add(result_btn )
        self._kb.row(refresh_score, minus_delta_button, plus_delta_button)

        return self._kb
