from abc import ABC
from abc import abstractmethod

from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup

from data.state import State
from data.user import User
from utils import i2e
from utils import MINUS
from utils import PLUS


class MarkupStrategy(ABC):
    @abstractmethod
    def as_markup(self) -> InlineKeyboardMarkup | None:
        pass


class ChooseIncrementMarkupStrategy(MarkupStrategy):

    def __init__(self, user: User) -> None:
        self.user = user

    def as_markup(self) -> InlineKeyboardMarkup | None:
        kb = InlineKeyboardMarkup()

        default_increment_btn = InlineKeyboardButton(
                f'Default: {i2e(1)}',
                callback_data='setupdelta 1',
            )
        delta_five_btn = InlineKeyboardButton(
                i2e(5),
                callback_data='setupdelta 5',
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

        kb.add(default_increment_btn)
        kb.add(delta_five_btn)
        kb.add(delta_ten_btn)
        kb.add(delta_fifteen_btn)
        kb.add(custom_increment_btn)
        kb.add(back_btn)
        return kb


class CustomIncrementMarkupStrategy(MarkupStrategy):
    def as_markup(self) -> InlineKeyboardMarkup | None:
        return None


class ProgressMarkupStrategy(MarkupStrategy):

    def __init__(self, user: User) -> None:
        self.user = user

    def as_markup(self) -> InlineKeyboardMarkup | None:
        kb = InlineKeyboardMarkup()
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

        if self.user.result != 0:
            kb.row(refresh_score)
        kb.row(update_increment_btn)

        kb.add(result_btn)
        kb.row(minus_delta_button, plus_delta_button)

        return kb


class UserKeyboard:
    def __init__(self, user: User, markup_strategy: MarkupStrategy):
        self.user = user
        self._kb = InlineKeyboardMarkup()
        self.markup_strategy = markup_strategy

    def create_markup(self):
        return self.markup_strategy.as_markup()


def init_user_keyboard(user: User) -> UserKeyboard:

    strategy_mapping = {
        State.WELCOME.value: ProgressMarkupStrategy(user),
        State.CHOOSE_INCREMENT.value: ChooseIncrementMarkupStrategy(user),
        State.PROGRESS.value: ProgressMarkupStrategy(user),
        State.CUSTOM_INCREMENT.value: CustomIncrementMarkupStrategy()
    }

    return UserKeyboard(user, strategy_mapping[user.current_state])
