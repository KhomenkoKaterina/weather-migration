"""Зчитування CSV (Kaggle: Global Weather Repository) і запис у БД."""
from sqlalchemy.orm import Session

from app.models import Weather, Wind, WindDirection
from app.repositories.weather_repository import WeatherRepository
from app.services.outside_service import should_go_outside
from app.services.parsing import (chunks, read_rows, to_datetime, to_float,
                                  to_int, to_time)

BATCH = 1000


def import_csv(session: Session, path: str) -> int:
    repo, total = WeatherRepository(session), 0
    for chunk in chunks(read_rows(path), BATCH):
        items = []
        for r in chunk:
            wind_kph = to_float(r["wind_kph"])
            gust_kph = to_float(r.get("gust_kph", ""))
            items.append(Weather(
                country=r["country"].strip(),
                location_name=r["location_name"].strip(),
                latitude=to_float(r.get("latitude", "")),
                longitude=to_float(r.get("longitude", "")),
                timezone=(r.get("timezone") or None),
                last_updated_epoch=to_int(r.get("last_updated_epoch", "")),
                last_updated=to_datetime(r["last_updated"]),
                temperature_celsius=to_float(r.get("temperature_celsius", "")),
                temperature_fahrenheit=to_float(r.get("temperature_fahrenheit", "")),
                condition_text=(r.get("condition_text") or None),
                sunrise=to_time(r.get("sunrise", "")),
                sunset=to_time(r.get("sunset", "")),
                wind=Wind(
                    wind_mph=to_float(r["wind_mph"]),
                    wind_kph=wind_kph,
                    wind_degree=to_int(r["wind_degree"]),
                    wind_direction=WindDirection(r["wind_direction"].strip()),
                    gust_mph=to_float(r.get("gust_mph", "")),
                    gust_kph=gust_kph,
                    go_outside=should_go_outside(wind_kph, gust_kph),
                ),
            ))
        repo.add_many(items)
        session.commit()
        total += len(items)
    return total