"""Допоміжні функції для зчитування CSV."""
import csv
from datetime import datetime, time
from itertools import islice
from typing import Iterator, Optional


def to_float(v: str) -> Optional[float]:
    v = (v or "").strip()
    return float(v) if v else None


def to_int(v: str) -> Optional[int]:
    v = (v or "").strip()
    return int(float(v)) if v else None


def to_time(v: str) -> Optional[time]:
    try:
        return datetime.strptime((v or "").strip(), "%I:%M %p").time()
    except ValueError:
        return None  # напр. "No sunrise" у полярних регіонах


def to_datetime(v: str) -> datetime:
    return datetime.strptime(v.strip(), "%Y-%m-%d %H:%M")


def read_rows(path: str) -> Iterator[dict]:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        yield from csv.DictReader(fh)


def chunks(it, n):
    while chunk := list(islice(it, n)):
        yield chunk