import datetime as dt

from data import db_session
from data.state import State
from data.user import User


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
        state: State | None = None,
        delta: int | None = None,
        result: int | None = None
) -> User:
    session = db_session.create_session()

    try:
        user = get_user_by_userid(userid=userid)
        user.delta = delta if delta is not None else user.delta
        user.current_state = state.value if state is not None else user.current_state
        user.result = result if result is not None else user.result
        user.update_date = dt.datetime.now()

        session.add(user)
        session.commit()

        return user

    finally:
        session.close()


def get_user_by_userid(userid: int) -> User | None:
    session = db_session.create_session()

    try:
        return session.query(User).where(User.userid == userid).first()
    finally:
        session.close()
