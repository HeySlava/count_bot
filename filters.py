import utils
from data.state import State
from exc import UserNotFound
from services import user_service


def is_user_stored_before(userid: int) -> bool:
    try:
        user_service.get_user_by_userid(userid)
    except UserNotFound:
        return False
    else:
        return True


def filter_by_state(userid: int, compare_state: State) -> bool:
    user = user_service.get_user_by_userid(userid)
    return user.current_state == compare_state.value


def check_user_custom_increment(text: str) -> bool:
    try:
        utils.try_positive_int(text)
    except ValueError:
        return False
    else:
        return True
