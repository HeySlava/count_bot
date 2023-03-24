from pydantic import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    token: str = ''
    admin_id: int = 0
    conn_str: str
    debug: bool = False

    class Config:
        env_prefix = 'counter_'
        env_file='.env',
        env_file_encoding='utf-8'


DBDIR = Path('db')
DBDIR.mkdir(exist_ok=True, parents=True)
DBFILE = DBDIR / 'count.sqlite'
_CONN_STR = f'sqlite:///{DBFILE.as_posix()}'


settings = Settings(
        conn_str=_CONN_STR,
    )
