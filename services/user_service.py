import datetime as dt
from typing import Optional

from sqlalchemy.exc import NoResultFound

from data import db_session
from data.state import State
from data.user import User
from exc import UserNotFound


class UserNotFoundError(Exception):
    pass


def create_user(userid: int, state: State) -> User:
    session = db_session.create_session()

    try:
        user = User()
        user.userid = userid
        user.current_state = state.value
        user.result = 0

        session.add(user)
        session.commit()

        return user

    finally:
        session.close()


def update_user(
        userid: int,
        state: Optional[State] = None,
        delta: Optional[int] = None,
        result: Optional[int] = None
) -> User:
    session = db_session.create_session()

    try:
        user = get_user_by_userid(userid=userid)
        if not user:
            raise UserNotFoundError(userid)
        user.delta = delta if delta is not None else user.delta
        user.current_state = state.value if state else user.current_state
        user.result = result if result is not None else user.result
        user.update_date = dt.datetime.now()

        session.add(user)
        session.commit()

        return user

    finally:
        session.close()


def get_user_by_userid(userid: int) -> User:
    session = db_session.create_session()

    try:
        return session.query(User).where(User.userid == userid).one()
    except NoResultFound:
        raise UserNotFound
    finally:
        session.close()
