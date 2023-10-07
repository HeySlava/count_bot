import datetime as dt

from data import db_session
from data.user import User


def update_result(userid: int, mode: str = '') -> User:
    session = db_session.create_session()

    user = session.query(User).where(User.userid == userid).one()

    try:
        if not mode:
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
