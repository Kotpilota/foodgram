# Foodgram - "Продуктовый помощник" 

Foodgram - это веб-сервис, где пользователи могут публиковать свои рецепты, добавлять чужие рецепты в избранное, подписываться на других авторов и формировать список покупок для выбранных рецептов.
### Сайт
https://kotpilota-foodgram.serveblog.net/
### Функциональность
- Создание, просмотр, редактирование и удаление рецептов
- Фильтрация рецептов по тегам
- Добавление рецептов в избранное
- Подписка на авторов
- Формирование и скачивание списка покупок (в TXT формате)
- Регистрация и авторизация пользователей
- Генерация коротких ссылок на рецепты
- Возможность добавления аватаров для пользователей

## Технический стек

### Бэкенд
- Python 3.9
- Django 3.2
- Django REST Framework
- PostgreSQL
- Docker
- Gunicorn
- Nginx

### Фронтенд
- React
- JavaScript
- HTML/CSS

### Инфраструктура
- Docker
- Docker Compose
- GitHub Actions (CI/CD)
- Nginx
- Gunicorn

## Инфраструктура проекта

Проект использует Docker и Docker Compose для запуска в изолированных контейнерах:
- **backend** - API проекта на Django REST Framework
- **frontend** - клиентская часть на React
- **nginx** - веб-сервер
- **db** - база данных PostgreSQL

## Запуск проекта

### Требования
- Docker и Docker Compose
- Git

### Локальный запуск

1. Клонировать репозиторий:
```bash
git clone https://github.com/Kotpilota/foodgram.git
cd foodgram
```

2. Создать файл `.env` в корневой директории проекта со следующими переменными окружения:
```
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_NAME=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=127.0.0.1,localhost
```

3. Запустить проект:
```bash
cd infra
docker-compose up -d
```

4. После успешного запуска API проекта будет доступен по адресу `http://localhost/api/`, а документация по адресу `http://localhost/api/docs/`.

## Структура API

Полная документация API доступна по эндпоинту `/api/docs/` после запуска проекта.

Основные эндпоинты:

- `/api/users/` - управление пользователями
- `/api/tags/` - получение списка тегов
- `/api/ingredients/` - получение списка ингредиентов
- `/api/recipes/` - управление рецептами
- `/api/recipes/{id}/favorite/` - добавление/удаление рецепта из избранного
- `/api/recipes/{id}/shopping_cart/` - добавление/удаление рецепта из списка покупок
- `/api/recipes/download_shopping_cart/` - скачивание списка покупок
- `/api/users/subscriptions/` - получение списка подписок
- `/api/users/{id}/subscribe/` - подписка/отписка от автора

## Автор

- [kotpilota](https://github.com/kotpilota) - разработчик