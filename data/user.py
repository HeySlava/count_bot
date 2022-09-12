import sqlalchemy as sa
import datetime as dt

from data.basemodel import Base


class User(Base):
    __tablename__ = 'users'

    userid: int = sa.Column(sa.Integer, primary_key=True)
    result: int = sa.Column(sa.Integer, default=0)
    delta: int = sa.Column(sa.Integer)
    current_state: int = sa.Column(sa.Integer, default=0)

    create_date: dt.datetime = sa.Column(sa.Integer, default=dt.datetime.now)
    update_date: dt.datetime = sa.Column(sa.Integer, default=dt.datetime.now)

    def __repr__(self):
        return f'<User_{self.userid}>'

    def to_dict(self):
        return self.__dict__
