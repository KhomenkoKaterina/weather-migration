"""Консольний інтерфейс.

python -m app.cli.main import --file data/GlobalWeatherRepository.csv
python -m app.cli.main search --country Ukraine --date 2024-05-16 [--location Kyiv] [--direction NW]
"""
import argparse
from datetime import date

from app.db import get_session_factory
from app.services.import_service import import_csv
from app.services.weather_service import WeatherService


def main() -> None:
    p = argparse.ArgumentParser(prog="weather")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("import"); s.add_argument("--file", required=True)
    s = sub.add_parser("search")
    s.add_argument("--country", required=True)
    s.add_argument("--date", required=True, type=date.fromisoformat)
    s.add_argument("--location")
    s.add_argument("--direction")
    a = p.parse_args()

    with get_session_factory()() as session:
        if a.cmd == "import":
            print(f"Завантажено рядків: {import_csv(session, a.file)}")
        else:
            found = WeatherService(session).find(a.country, a.date, a.location, a.direction)
            if not found:
                print("Нічого не знайдено.")
            for w in found:
                print(WeatherService.format(w), end="\n\n")
            print(f"Всього записів: {len(found)}")


if __name__ == "__main__":
    main()