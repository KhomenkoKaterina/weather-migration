from datetime import date, datetime, time, timedelta
from typing import Optional, Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Weather, WindDirection


class WeatherRepository:
    """Шар доступу до даних: лише запити до БД, без бізнес-логіки."""

    def __init__(self, session: Session):
        self.session = session

    def add_many(self, items: Sequence[Weather]) -> None:
        self.session.add_all(items)

    def search(self, country: str, day: date, location: Optional[str] = None,
               direction: Optional[WindDirection] = None) -> list[Weather]:
        start = datetime.combine(day, time.min)
        end = start + timedelta(days=1)
        stmt = (
            select(Weather)
            .where(func.lower(Weather.country) == country.lower(),
                   Weather.last_updated >= start,
                   Weather.last_updated < end)
            .order_by(Weather.location_name, Weather.last_updated)
        )
        if location:
            stmt = stmt.where(func.lower(Weather.location_name) == location.lower())
        if direction:
            stmt = stmt.where(Weather.wind_direction == direction)
        return list(self.session.execute(stmt).scalars().all())