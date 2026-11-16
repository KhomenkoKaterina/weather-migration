"""Етап 1: одна таблиця weather з усіма відібраними колонками

Revision ID: 0001
Revises:
"""
import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

DIRS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]


def upgrade() -> None:
    op.create_table(
        "weather",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("country", sa.String(100), nullable=False),
        sa.Column("location_name", sa.String(150), nullable=False),
        sa.Column("latitude", sa.Float),
        sa.Column("longitude", sa.Float),
        sa.Column("timezone", sa.String(64)),
        sa.Column("last_updated_epoch", sa.BigInteger),
        sa.Column("last_updated", sa.DateTime, nullable=False),
        sa.Column("temperature_celsius", sa.Float),
        sa.Column("temperature_fahrenheit", sa.Float),
        sa.Column("condition_text", sa.String(100)),
        sa.Column("sunrise", sa.Time),
        sa.Column("sunset", sa.Time),
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
    op.create_index("ix_weather_country_last_updated", "weather", ["country", "last_updated"])


def downgrade() -> None:
    op.drop_index("ix_weather_country_last_updated", table_name="weather")
    op.drop_table("weather")