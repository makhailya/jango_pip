# Интернет-магазин

Веб-приложение интернет-магазина на Django с Bootstrap.

## Описание проекта

Это учебный проект интернет-магазина, разработанный в рамках курса по Django. Проект включает:

- Главную страницу с товарами
- Страницу контактов с формой обратной связи
- Адаптивный дизайн на основе Bootstrap 5

## Технологии

- **Python 3.10+**
- **Django 4.2+**
- **Bootstrap 5.3**
- **HTML5 / CSS3**

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <url-репозитория>
cd internet_shop
```

### 2. Создание виртуального окружения

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Применение миграций

```bash
python manage.py migrate
```

### 5. Запуск сервера

```bash
python manage.py runserver
```

Сайт будет доступен по адресу: `http://127.0.0.1:8000/`

## Структура проекта

```
internet_shop/
├── config/              # Настройки проекта
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── catalog/             # Приложение каталога
│   ├── templates/
│   │   └── catalog/
│   │       ├── base.html
│   │       ├── home.html
│   │       └── contacts.html
│   ├── views.py
│   ├── urls.py
│   └── models.py
├── manage.py
├── requirements.txt
└── README.md
```

## Доступные страницы

- **Главная:** `/` — отображает список товаров
- **Контакты:** `/contacts/` — форма обратной связи

## Разработка

### Ветвление (GitFlow)

- `main` — продакшн версия
- `develop` — разработка
- `feature/*` — новые функции

### Создание новой ветки

```bash
git checkout develop
git checkout -b feature/new-feature
```

### Коммиты

Следуем соглашению о коммитах:
```
feat: добавлена новая функция
fix: исправлена ошибка
docs: обновлена документация
style: форматирование кода
```

## Первоначальная настройка

1. Клонируй репозиторий:
```bash
git clone <url>
cd internet_shop
```

2. Создай и активируй виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

3. Установи зависимости:
```bash
pip install -r requirements.txt
```

4. Создай файл .env на основе .env.sample:
```bash
cp .env.sample .env  # Mac/Linux
copy .env.sample .env  # Windows
```

5. Отредактируй .env, указав свои настройки БД

6. Создай базу данных в PostgreSQL:
```sql
CREATE DATABASE internet_shop_db;
CREATE USER shop_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE internet_shop_db TO shop_user;
```

7. Примени миграции:
```bash
python manage.py migrate
```

8. Создай суперпользователя:
```bash
python manage.py createsuperuser
```

9. Загрузи тестовые данные:
```bash
python manage.py load_data
```

10. Запусти сервер:
```bash
python manage.py runserver
```

## Автор

makhailya

## Лицензия

MIT License
