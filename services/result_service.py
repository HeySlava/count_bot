import datetime as dt
from data import db_session
from data.user import User
from services.user_service import get_user_by_userid


def update_result(userid: int, mode: str = None) -> User | None:
    session = db_session.create_session()

    user = get_user_by_userid(userid)

    if not user:
        return None

    try:
        if mode is None:
            user.result = 0
        if mode == 'plus':
            user.result += user.delta
        if mode == 'minus':
            user.result -= user.delta
        user.update_date = dt.datetime.now()

        session.add(user)
        session.commit()

        return user
    finally:
        session.close()
