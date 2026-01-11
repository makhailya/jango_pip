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

## Автор

Ваше имя

## Лицензия

MIT License
