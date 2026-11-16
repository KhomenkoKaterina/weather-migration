"""Міграція даних з однієї СУБД в іншу (Postgres <-> MySQL).

python -m scripts.copy_db --source postgresql+psycopg2://... --target mysql+pymysql://...

1) на цільовій БД накочуються ті самі alembic-міграції (схема ідентична),
2) дані копіюються порціями зі збереженням id,
3) для Postgres скидаються sequence,
4) звіряються кількості рядків.
"""
import argparse
import os

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, func, select, text

from app.models import Weather, Wind

CHUNK = 5000
TABLES = (Weather.__table__, Wind.__table__)   # спочатку батьківська таблиця


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--target", required=True)
    a = ap.parse_args()

    os.environ["DATABASE_URL"] = a.target
    command.upgrade(Config("alembic.ini"), "head")

    src, dst = create_engine(a.source), create_engine(a.target)
    with dst.connect() as c:
        if c.execute(select(func.count()).select_from(Weather.__table__)).scalar():
            raise SystemExit("Цільова БД не порожня: зупиняюсь, щоб нічого не перезаписати.")

    for table in TABLES:
        with src.connect() as s, dst.begin() as d:
            res = s.execution_options(stream_results=True).execute(select(table)).mappings()
            while chunk := res.fetchmany(CHUNK):
                d.execute(table.insert(), [dict(r) for r in chunk])

    if dst.dialect.name == "postgresql":
        with dst.begin() as d:
            for t in ("weather", "wind"):
                d.execute(text(
                    f"SELECT setval(pg_get_serial_sequence('{t}','id'), "
                    f"COALESCE((SELECT MAX(id) FROM {t}), 1))"))

    for table in TABLES:
        with src.connect() as s, dst.connect() as d:
            n1 = s.execute(select(func.count()).select_from(table)).scalar()
            n2 = d.execute(select(func.count()).select_from(table)).scalar()
            print(f"{table.name}: source={n1} target={n2} {'OK' if n1 == n2 else 'MISMATCH'}")


if __name__ == "__main__":
    main()