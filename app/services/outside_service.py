"""Бізнес-логіка: «Чи варто виходити на вулицю».

Виходити можна, якщо середній вітер <= 10 м/с (36 км/год)
і пориви <= 15 м/с (54 км/год). Якщо поривів немає, враховується лише середній вітер.
Ті самі пороги (в км/год) зашиті в міграцію 0003 для вже наявних рядків.
"""
from typing import Optional

MAX_WIND_KPH = 36.0   # 10 м/с
MAX_GUST_KPH = 54.0   # 15 м/с


def should_go_outside(wind_kph: float, gust_kph: Optional[float] = None) -> bool:
    if wind_kph > MAX_WIND_KPH:
        return False
    if gust_kph is not None and gust_kph > MAX_GUST_KPH:
        return False
    return True