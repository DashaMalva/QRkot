# Учебный проект QRKot
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/index.html)
[![Google Sheets](https://img.shields.io/badge/Google%20Sheets-34A853?style=for-the-badge&logo=google-sheets&logoColor=white)](https://developers.google.com/sheets/api/guides/concepts)
[![Google Drive](https://img.shields.io/badge/Google%20Drive-4285F4?style=for-the-badge&logo=googledrive&logoColor=white)](https://developers.google.com/drive/api/guides/about-sdk)

```QRKot``` - это приложение для Благотворительного фонда, реализованное на фреймворке FastAPI.<br>
Цель проекта - отработать навыки работы с FastAPI, SQLAlchemy и GoogleAPI.

## Технологии
- Python 3.10
- FastAPI 0.78.0
- Uvicorn 0.17.6
- SQLAlchemy 1.4.36
- Alembic 1.7.7
- FastAPI Users 10.0.4
- Aiogoogle 4.2.0
- Google Sheet API v4
- Google Drive API v3

## Описание приложения

Благотворительный фонд собирает пожертвования на различные целевые проекты.
У каждого проекта есть название, описание и сумма, которую планируется собрать. 
Каждый пользователь может сделать пожертвование и сопроводить его комментарием.
Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму.
Когда проект набирает необходимую сумму, он закрывается.


### Возможности приложения:
- создание благотворительных проектов,
- создание и автоматическое распределение между проектами пожертвований пользователей,
- система управления пользователями,
- создание отчета по закрытым проектам в виде гугл-таблицы.

### Спецификация приложения
Документация проекта доступна после запуска проекта по адресам ```/docs``` и ```/redoc```


### База данных
В проекте настроено асинхронное подключение к базе данных через SQLAlchemy ORM.<br>
Миграции базы данных настроены через библиотеку Alembic.


### Формирования отчета в гугл-таблицы
#### Подключение к GoogleAPI
Для работы с Google API необходимо в Google Cloud Platform создать проект с сервисным аккаунтом и подключенными Google Drive API и Google Sheets API. У проекта нужно сформировать JSON-файл с ключом доступа к сервисному аккаунту и перенести его данные в файл .env.<br>
В .env файл также следует добавить адрес личного гугл-аккаунта для выдачи прав доступа к сформированному отчету.<br>
Пример наполнения файла .env:
```
DATABASE_URL=sqlite+aiosqlite:///./db.sqlite
EMAIL=user@gmail.com
TYPE=
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY="..."
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=
```

## Как развернуть проект на компьютере:
1. Клонировать репозиторий c GitHub на компьютер и перейти в него в командной строке
```
$ git clone https://github.com/DashaMalva/QRkot.git
$ cd QRkot
```
2. Создать и активировать виртуальное окружение
```
# Windows
$ python -m venv venv
$ source venv/Scripts/activate

# Linux
python3 -m venv venv
source venv/bin/activate
```
3. Обновить менеджер пакетов pip
```
$ python -m pip install --upgrade pip
```
4. Установить зависимости из requirements.txt
```
$ pip install -r requirements.txt
```
5. Создать файл .env с переменными окружения. Пример наполнения:
```
DATABASE_URL=sqlite+aiosqlite:///./db.sqlite
SECRET=secret
```
6. Создать базу данных
```
$ alembic upgrade head
```
7. Запустить приложение
```
$ uvicorn app.main:app
```

### Лицензия
The MIT License (MIT)

### Автор проекта
Студент Яндекс.Практикум,<br>
Дарья Матвиевская
