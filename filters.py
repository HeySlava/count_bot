from exc import UserNotFound
from services import user_service


def is_user_stored_before(userid: int) -> bool:
    try:
        user_service.get_user_by_userid(userid)
    except UserNotFound:
        return False
    else:
        return True
