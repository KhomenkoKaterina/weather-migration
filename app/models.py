import enum
from datetime import datetime, time
from typing import Optional

from sqlalchemy import BigInteger, DateTime, Enum, Float, Index, Integer, String, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class WindDirection(str, enum.Enum):
    N = "N"; NNE = "NNE"; NE = "NE"; ENE = "ENE"
    E = "E"; ESE = "ESE"; SE = "SE"; SSE = "SSE"
    S = "S"; SSW = "SSW"; SW = "SW"; WSW = "WSW"
    W = "W"; WNW = "WNW"; NW = "NW"; NNW = "NNW"


class Weather(Base):
    __tablename__ = "weather"
    __table_args__ = (Index("ix_weather_country_last_updated", "country", "last_updated"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False)          # текстова
    location_name: Mapped[str] = mapped_column(String(150), nullable=False)
    latitude: Mapped[Optional[float]] = mapped_column(Float)
    longitude: Mapped[Optional[float]] = mapped_column(Float)
    timezone: Mapped[Optional[str]] = mapped_column(String(64))
    last_updated_epoch: Mapped[Optional[int]] = mapped_column(BigInteger)
    last_updated: Mapped[datetime] = mapped_column(DateTime, nullable=False)    # дата
    temperature_celsius: Mapped[Optional[float]] = mapped_column(Float)
    temperature_fahrenheit: Mapped[Optional[float]] = mapped_column(Float)
    condition_text: Mapped[Optional[str]] = mapped_column(String(100))
    sunrise: Mapped[Optional[time]] = mapped_column(Time)                      # час
    sunset: Mapped[Optional[time]] = mapped_column(Time)

    # --- категорія «вітер» ---
    wind_mph: Mapped[float] = mapped_column(Float, nullable=False)
    wind_kph: Mapped[float] = mapped_column(Float, nullable=False)             # дробове
    wind_degree: Mapped[int] = mapped_column(Integer, nullable=False)          # ціле
    # native_enum=False -> VARCHAR(3): однаково працює в Postgres і MySQL
    wind_direction: Mapped[WindDirection] = mapped_column(                     # enumeration
        Enum(WindDirection, native_enum=False, length=3, create_constraint=False),
        nullable=False,
    )
    gust_mph: Mapped[Optional[float]] = mapped_column(Float)
    gust_kph: Mapped[Optional[float]] = mapped_column(Float)