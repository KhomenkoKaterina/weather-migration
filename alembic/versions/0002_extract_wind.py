"""Етап 2: колонки вітру виносяться в таблицю wind (дані переносяться)

Revision ID: 0002
Revises: 0001
"""
import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None

DIRS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
WIND_COLS = ["wind_mph", "wind_kph", "wind_degree", "wind_direction", "gust_mph", "gust_kph"]


def upgrade() -> None:
    # 1) нова таблиця
    op.create_table(
        "wind",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("weather_id", sa.Integer,
                  sa.ForeignKey("weather.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("wind_mph", sa.Float, nullable=False),
        sa.Column("wind_kph", sa.Float, nullable=False),
        sa.Column("wind_degree", sa.Integer, nullable=False),
        sa.Column("wind_direction",
                  sa.Enum(*DIRS, name="wind_direction", native_enum=False,
                          length=3, create_constraint=False),
                  nullable=False),
        sa.Column("gust_mph", sa.Float),
        sa.Column("gust_kph", sa.Float),
    )
    # 2) перенесення даних (стандартний SQL, однаково для Postgres і MySQL)
    op.execute(
        "INSERT INTO wind (weather_id, wind_mph, wind_kph, wind_degree, wind_direction, gust_mph, gust_kph) "
        "SELECT id, wind_mph, wind_kph, wind_degree, wind_direction, gust_mph, gust_kph FROM weather"
    )
    # 3) лише після копіювання прибираємо колонки зі старої таблиці
    with op.batch_alter_table("weather") as batch:
        for c in WIND_COLS:
            batch.drop_column(c)


def downgrade() -> None:
    with op.batch_alter_table("weather") as batch:
        batch.add_column(sa.Column("wind_mph", sa.Float))
        batch.add_column(sa.Column("wind_kph", sa.Float))
        batch.add_column(sa.Column("wind_degree", sa.Integer))
        batch.add_column(sa.Column("wind_direction", sa.String(3)))
        batch.add_column(sa.Column("gust_mph", sa.Float))
        batch.add_column(sa.Column("gust_kph", sa.Float))
    sets = ", ".join(
        f"{c} = (SELECT w.{c} FROM wind w WHERE w.weather_id = weather.id)" for c in WIND_COLS
    )
    op.execute(f"UPDATE weather SET {sets}")
    with op.batch_alter_table("weather") as batch:
        batch.alter_column("wind_mph", existing_type=sa.Float, nullable=False)
        batch.alter_column("wind_kph", existing_type=sa.Float, nullable=False)
        batch.alter_column("wind_degree", existing_type=sa.Integer, nullable=False)
        batch.alter_column("wind_direction", existing_type=sa.String(3), nullable=False)
    op.drop_table("wind")