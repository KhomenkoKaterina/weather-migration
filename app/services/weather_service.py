from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from app.models import Weather, WindDirection
from app.repositories.weather_repository import WeatherRepository


class WeatherService:
    def __init__(self, session: Session):
        self.repo = WeatherRepository(session)

    def find(self, country: str, day: date, location: Optional[str] = None,
             direction: Optional[str] = None) -> list[Weather]:
        d = WindDirection(direction.upper()) if direction else None
        return self.repo.search(country, day, location, d)

    @staticmethod
    def format(w: Weather) -> str:
        x = w.wind
        return (
            f"{w.country} / {w.location_name} @ {w.last_updated:%Y-%m-%d %H:%M}\n"
            f"  Координати: {w.latitude}, {w.longitude}; часовий пояс: {w.timezone}\n"
            f"  Температура: {w.temperature_celsius} °C ({w.temperature_fahrenheit} °F), {w.condition_text}\n"
            f"  Схід/захід сонця: {w.sunrise} / {w.sunset}\n"
            f"  Вітер: {x.wind_kph} км/год ({x.wind_mph} mph), {x.wind_degree}° "
            f"{x.wind_direction.value}, пориви {x.gust_kph} км/год"
        )