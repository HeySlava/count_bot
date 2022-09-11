import sqlalchemy as sa
from sqlalchemy import orm

Base = orm.declarative_base()


class User(Base):
    __tablename__ = 'users'

    userid: int = sa.Column(sa.Integer, primary_key=True)
    result: int = sa.Column(sa.Integer, default=0)
    delta: int = sa.Column(sa.Integer)


    def __repr__(self):
        return f'<User{self.userid} with result={self.result} and delta={self.delta}>'

    def to_dict(self):
        return self.__dict__
