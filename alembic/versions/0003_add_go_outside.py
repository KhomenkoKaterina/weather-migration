"""Етап 3: wind.go_outside («Чи варто виходити на вулицю») + заповнення

Revision ID: 0003
Revises: 0002
"""
import sqlalchemy as sa
from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None

# Заморожені пороги (км/год): 10 м/с та 15 м/с. Міграція не імпортує код застосунку,
# щоб її результат не змінювався разом з майбутніми правками сервісу.
MAX_WIND_KPH = 36.0
MAX_GUST_KPH = 54.0


def upgrade() -> None:
    # Крок A: колонка з дефолтом "ні": існуючі рядки одразу валідні
    op.add_column("wind", sa.Column("go_outside", sa.Boolean, nullable=False,
                                    server_default=sa.false()))
    # Крок B: заповнити наявні рядки за формулою
    wind = sa.table("wind",
                    sa.column("wind_kph", sa.Float),
                    sa.column("gust_kph", sa.Float),
                    sa.column("go_outside", sa.Boolean))
    ok = sa.and_(wind.c.wind_kph <= MAX_WIND_KPH,
                 sa.or_(wind.c.gust_kph.is_(None), wind.c.gust_kph <= MAX_GUST_KPH))
    op.execute(wind.update().values(go_outside=sa.case((ok, sa.true()), else_=sa.false())))


def downgrade() -> None:
    op.drop_column("wind", "go_outside")