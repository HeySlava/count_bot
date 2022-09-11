import sqlalchemy as sa

import db_session

from models import User


db_session.global_init('sqlite:///count.sqlite')


def create_user(userid: int, level: int, delta: int = 0) -> User:
    session = db_session.create_session()

    try:
        if user := get_user_by_userid(userid=userid):
            user.current_level = level
            user.delta = delta
        else:
            user = User()
            user.userid = userid
            user.delta = delta
            user.current_level = level

        session.add(user)
        session.commit()

        return user

    finally:
        session.close()


def change_result(userid: int, mode: str) -> User | None:
    session = db_session.create_session()

    user = get_user_by_userid(userid)

    if not user:
        return None

    try:
        if mode == 'plus':
            user.result += user.delta
        if mode == 'minus':
            user.result -= user.delta

        session.add(user)
        session.commit()

        return user
    finally:
        session.close()


def get_user_by_userid(userid: int) -> User | None:
    session = db_session.create_session()

    try:
        return session.scalars(sa.select(User).filter(User.userid == userid)).first()
    finally:
        session.close()


def refresh_score(userid: int) -> User:
    session = db_session.create_session()

    try:
        user = get_user_by_userid(userid=userid)
        if user.result == 0:
            return user
        user.result = 0

        session.add(user)
        session.commit()

        return user

    finally:
        session.close()
