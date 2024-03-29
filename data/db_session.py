import sqlalchemy as sa
from sqlalchemy import orm

from data.basemodel import Base


_factory = None


def global_init(conn_str: str, debug: bool):
    global _factory

    if not conn_str.strip():
        raise Exception('You have to specify conn_str, but your {!r:conn_str}')

    engine = sa.create_engine(conn_str, echo=debug)

    _factory = orm.sessionmaker(bind=engine)

    Base.metadata.create_all(engine)


def create_session():
    global _factory
    if not _factory:
        raise Exception('You must call global_init() before using this method')

    session: orm.Session = _factory()
    session.expire_on_commit = False
    return session
