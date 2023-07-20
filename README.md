## Проект QRKot

Приложение для Благотворительного фонда поддержки котиков QRKot.  
Фонд собирает пожертвования на различные целевые проекты: на медицинское  
обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в  
подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные  
с поддержкой кошачьей популяции.  

## Технологии
* Python 3.10.10  

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/shmyrev/cat_charity_fund.git
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создайте и заполните файл .env (пример .env.sample):
```
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=secret
FIRST_SUPERUSER_EMAIL=admin@admin.com
FIRST_SUPERUSER_PASSWORD=admin
```

Выполните миграции:
```
alembic upgrade head 
```

Запустите проект:
```
uvicorn app.main:app --reload
```

## Примеры запросов:
GET-запрос:
```
/charity_project/
```

Request:
```
[
  {
    "name": "string",
    "description": "string",
    "full_amount": 0,
    "id": 0,
    "invested_amount": 0,
    "fully_invested": true,
    "create_date": "2019-08-24T14:15:22Z",
    "close_date": "2019-08-24T14:15:22Z"
  }
]
```

POST-запрос:
```
/charity_project/
```

Request:
```
{
  "name": "string",
  "description": "string",
  "full_amount": 0
}
```