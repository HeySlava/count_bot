from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup

from data.state import State
from data.user import User
from utils import i2e
from utils import MINUS
from utils import PLUS


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

        if self.user.current_state == State.CUSTOM_INCREMENT.value:
            return self._custom_increment_markup()

    def _welcome_markup(self):
        return self._progress_markup()

        setup_increment_btn = InlineKeyboardButton(
                'Setup increment',
                callback_data=str(State.CHOOSE_INCREMENT.value),
            )

        self._kb.add(setup_increment_btn)
        return self._kb

    def _choose_increment_markup(self):
        default_increment_btn = InlineKeyboardButton(
                f'Default: {i2e(1)}', callback_data='setupdelta 1')

        delta_five_btn = InlineKeyboardButton(
                i2e(5), callback_data='setupdelta 5',
            )
        delta_ten_btn = InlineKeyboardButton(
                i2e(10), callback_data='setupdelta 10',
            )
        delta_fifteen_btn = InlineKeyboardButton(
                i2e(15), callback_data='setupdelta 15',
            )

        back_btn = InlineKeyboardButton(
                f'Leave current: {i2e(self.user.delta)}',
                callback_data=f'setupdelta {self.user.delta}',
            )
        custom_increment_btn = InlineKeyboardButton(
                'Type it by your own',
                callback_data=str(State.CUSTOM_INCREMENT.value),
            )

        self._kb.add(default_increment_btn)
        self._kb.add(delta_five_btn)
        self._kb.add(delta_ten_btn)
        self._kb.add(delta_fifteen_btn)
        self._kb.add(custom_increment_btn)
        self._kb.add(back_btn)
        return self._kb

    def _custom_increment_markup(self):

        refresh = InlineKeyboardButton(
                'Refresh when you write new value', callback_data='/# TODO')
        return self._kb.add(refresh)

    def _progress_markup(self):

        update_increment_btn = InlineKeyboardButton(
                'Change increment',
                callback_data=str(State.CHOOSE_INCREMENT.value),
            )

        minus_delta_button = InlineKeyboardButton(
                MINUS + i2e(self.user.delta), callback_data='minus')

        result_btn = InlineKeyboardButton(
                i2e(self.user.result), callback_data=str(self.user.result))

        plus_delta_button = InlineKeyboardButton(
                PLUS + i2e(self.user.delta), callback_data='plus')

        refresh_score = InlineKeyboardButton(
                'Refresh score', callback_data='refresh_score')

        if not self.user.result == 0:
            self._kb.row(refresh_score)
        self._kb.row(update_increment_btn)

        self._kb.add(result_btn)
        self._kb.row(minus_delta_button, plus_delta_button)

        return self._kb
