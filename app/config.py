"""URL бази береться зі змінної середовища DATABASE_URL.

Postgres: postgresql+psycopg2://postgres:ПАРОЛЬ@localhost:5432/weather
MySQL:    mysql+pymysql://root:ПАРОЛЬ@localhost:3306/weather
"""
import os

DEFAULT_URL = "postgresql+psycopg2://1:postgres@localhost:5432/weather"


def get_database_url() -> str:
    return os.environ.get("DATABASE_URL", DEFAULT_URL)