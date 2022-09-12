import sqlalchemy as sa 

from sqlalchemy import orm

from data.basemodel import Base


def global_init(conn_str: str):
    global _factory

    if not conn_str.strip():
        raise Exception('You have to specify conn_str, but your {!r:conn_str}')

    engine = sa.create_engine(conn_str, echo=True)

    _factory = orm.sessionmaker(bind=engine)

    Base.metadata.create_all(engine)
    

def create_session():

    if not _factory:
        raise Exception('You must call global_init() before using this method')

    session: orm.Session = _factory()
    session.expire_on_commit = False
    return session
