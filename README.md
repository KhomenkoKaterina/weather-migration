# Global weather repository: міграція бази даних

Проєкт демонструє рефакторинг схеми бази даних на прикладі датасету погодних даних. Категорія «вітер» виноситься в окрему таблицю, а дані переносяться між PostgreSQL і MySQL з перевіркою цілісності.

## Датасет

[Global Weather Repository](https://www.kaggle.com/) (Kaggle), файл `GlobalWeatherRepository.csv`.

## Стек

- Python 3.x
- SQLAlchemy 2 (ORM)
- Alembic (міграції)
- PostgreSQL, MySQL
- Docker

## Архітектура

Проєкт побудовано за шаровим принципом:

```
cli (презентація) -> services (бізнес-логіка) -> repositories (доступ до даних)
                                                    -> models (ORM) + alembic (міграції)
```

- **cli**: точка входу, розбір аргументів, запуск сервісів.
- **services**: бізнес-логіка, зокрема формула `go_outside` і координація міграцій.
- **repositories**: запити до БД, без бізнес-логіки.
- **models**: ORM-моделі SQLAlchemy 2.
- **alembic**: ревізії схеми.

## Схема даних

**Таблиця `weather`** (основна):

| Колонка | Тип | Опис |
|---|---|---|
| `id` | integer, PK | Ідентифікатор рядка |
| `country` | text | Країна |
| `location_name` | text | Назва локації |
| `latitude`, `longitude` | float | Координати |
| `timezone` | text | Часовий пояс |
| `last_updated_epoch` | integer | Час оновлення (Unix epoch) |
| `last_updated` | date | Дата оновлення |
| `temperature_celsius`, `temperature_fahrenheit` | float | Температура |
| `condition_text` | text | Опис погоди |
| `sunrise`, `sunset` | time | Час сходу і заходу сонця |

**Таблиця `wind`** (категорія «вітер», винесена з `weather`):

| Колонка | Тип | Опис |
|---|---|---|
| `id` | integer, PK | Збігається з `weather.id` |
| `wind_mph`, `wind_kph` | float | Швидкість вітру |
| `wind_degree` | integer | Напрямок у градусах |
| `wind_direction` | VARCHAR(3) | Напрямок (enum на рівні ORM) |
| `gust_mph`, `gust_kph` | float | Пориви вітру |
| `go_outside` | boolean, default `false` | Чи можна виходити на вулицю |

Правило для `go_outside`: `true`, якщо швидкість вітру ≤ 10 м/с і пориви ≤ 15 м/с. <!-- TODO: перевірити одиниці. Датасет у миль/год і км/год, а пороги в м/с. Вкажи конкретну колонку та переведені пороги. -->

## Гілки і міграції

| Гілка | Опис |
|---|---|
| `stage-1-initial` | Початкова схема: одна таблиця `weather` з усіма колонками |
| `stage-2-extract-wind` | Створення `wind`, перенесення даних, видалення колонок вітру з `weather` |
| `stage-3-go-outside` | Додавання `go_outside` і заповнення за формулою |
| `stage-4-mysql` | Перенесення на MySQL |

### Міграція 1 -> 2

1. Створюється таблиця `wind`.
2. `INSERT ... SELECT` переносить дані з `weather` у `wind`.
3. Лише після копіювання колонки вітру видаляються з `weather`.

Міграція оборотна: `downgrade` повертає колонки і дані в `weather`.

### Міграція 2 -> 3

1. Колонка `go_outside` додається з `server_default = false`, тож існуючі рядки одразу валідні.
2. `UPDATE` проставляє значення за формулою.

### Міграція 3 -> 4

1. Схема та сама, MySQL-база порожня.
2. Ті самі міграції застосовуються до MySQL.
3. Дані копіюються зі збереженням `id`: спочатку `weather`, потім `wind`.
4. Кількість рядків звіряється з джерелом.

## Встановлення

```bash
git clone <repo-url>
cd <repo-name>
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Налаштування баз даних

```bash
export DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/weather"
# або для MySQL:
export DATABASE_URL="mysql+pymysql://user:password@localhost:3306/weather"
```

<!-- TODO: вказати, як задається URL: через змінну середовища чи конфіг -->

## Використання

```bash
# Застосувати всі міграції
alembic upgrade head

# Відкотити до попередньої ревізії
alembic downgrade -1

# Імпорт CSV
python -m cli import --file GlobalWeatherRepository.csv

# Перенесення з PostgreSQL в MySQL
python -m cli migrate --target mysql
```

<!-- TODO: звірити команди з твоїм cli -->

## Тести

```bash
pytest
```

<!-- TODO: описати, що покривають тести -->

## Структура проєкту

```
.
├── alembic/            # ревізії міграцій
├── cli/                # точка входу
├── services/           # бізнес-логіка
├── repositories/       # доступ до даних
├── models/             # ORM-моделі
├── tests/
├── alembic.ini
├── requirements.txt
└── README.md
```
