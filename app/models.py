import enum
from datetime import datetime, time
from typing import Optional

from sqlalchemy import (BigInteger, Boolean, DateTime, Enum, Float, ForeignKey, Index,
                        Integer, String, Time, false)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


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
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    location_name: Mapped[str] = mapped_column(String(150), nullable=False)
    latitude: Mapped[Optional[float]] = mapped_column(Float)
    longitude: Mapped[Optional[float]] = mapped_column(Float)
    timezone: Mapped[Optional[str]] = mapped_column(String(64))
    last_updated_epoch: Mapped[Optional[int]] = mapped_column(BigInteger)
    last_updated: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    temperature_celsius: Mapped[Optional[float]] = mapped_column(Float)
    temperature_fahrenheit: Mapped[Optional[float]] = mapped_column(Float)
    condition_text: Mapped[Optional[str]] = mapped_column(String(100))
    sunrise: Mapped[Optional[time]] = mapped_column(Time)
    sunset: Mapped[Optional[time]] = mapped_column(Time)

    wind: Mapped[Optional["Wind"]] = relationship(
        back_populates="weather", uselist=False, cascade="all, delete-orphan"
    )


class Wind(Base):
    __tablename__ = "wind"

    id: Mapped[int] = mapped_column(primary_key=True)
    weather_id: Mapped[int] = mapped_column(
        ForeignKey("weather.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    wind_mph: Mapped[float] = mapped_column(Float, nullable=False)
    wind_kph: Mapped[float] = mapped_column(Float, nullable=False)
    wind_degree: Mapped[int] = mapped_column(Integer, nullable=False)
    wind_direction: Mapped[WindDirection] = mapped_column(
        Enum(WindDirection, native_enum=False, length=3, create_constraint=False),
        nullable=False,
    )
    gust_mph: Mapped[Optional[float]] = mapped_column(Float)
    gust_kph: Mapped[Optional[float]] = mapped_column(Float)
    # «Чи варто виходити на вулицю»; дефолт на рівні БД = false («ні»)
    go_outside: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=false()
    )

    weather: Mapped["Weather"] = relationship(back_populates="wind")