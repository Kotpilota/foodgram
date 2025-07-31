# Foodgram

[![CI/CD Status](https://github.com/Kotpilota/foodgram/actions/workflows/main.yml/badge.svg)](https://github.com/Kotpilota/foodgram/actions)
[![Docker](https://img.shields.io/badge/docker-available-blue)](https://hub.docker.com/u/kotpilota)

**Foodgram** — это веб-приложение "Продуктовый помощник" для любителей кулинарии, где пользователи могут публиковать рецепты, подписываться на других авторов и формировать списки покупок. Проект демонстрирует полный цикл разработки веб-приложения с современной архитектурой.

## О проекте

Этот проект является дипломным заданием курса "Python-разработчик" от Яндекс.Практикум и показывает комплексный подход к разработке веб-приложения:

- **Цель**: Создание платформы для обмена кулинарными рецептами с социальными функциями
- **Задача**: Разработка полнофункционального REST API, настройка CI/CD и автоматический деплой
- **Результат**: Готовое к продакшену приложение с современной инфраструктурой

### Основной функционал
- Регистрация и аутентификация пользователей
- Создание, редактирование и публикация рецептов
- Загрузка изображений готовых блюд
- Система тегов для категоризации рецептов
- Подписки на других авторов рецептов
- Добавление рецептов в избранное
- Формирование и скачивание списка покупок
- Адаптивный интерфейс для всех устройств
- Пагинация и фильтрация контента

## Технологический стек

### Backend
- **Python 3.9** - основной язык разработки
- **Django 3.2** - веб-фреймворк
- **Django REST Framework 3.14** - API
- **Djoser** - система аутентификации
- **PostgreSQL 13** - база данных
- **Gunicorn** - WSGI сервер
- **Pillow** - обработка изображений

### Frontend  
- **React** - пользовательский интерфейс
- **Node.js 18** - среда выполнения JavaScript

### DevOps & Infrastructure
- **Docker & Docker Compose** - контейнеризация
- **Nginx** - веб-сервер и reverse proxy
- **GitHub Actions** - CI/CD автоматизация
- **Docker Hub** - реестр образов

## Быстрый старт

### Требования
- Docker и Docker Compose
- Git

### Локальный запуск

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/kotpilota/foodgram.git
cd foodgram
```

2. **Создайте файл окружения:**
```bash
cp .env.example .env
```

Заполните `.env` файл:
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=foodgram
DB_USER=foodgram_user
DB_PASSWORD=secure_password_here
DB_HOST=db
DB_PORT=5432
SECRET_KEY=your-super-secret-django-key
DEBUG=False
ALLOWED_HOSTS=127.0.0.1,localhost,yourdomain.com
```

3. **Запустите проект:**
```bash
docker compose up -d
```

4. **Выполните миграции и настройку:**
```bash
# Применить миграции
docker compose exec backend python manage.py migrate

# Собрать статические файлы
docker compose exec backend python manage.py collectstatic --noinput

# Создать суперпользователя
docker compose exec backend python manage.py createsuperuser

# Загрузить данные ингредиентов и тегов
docker compose exec backend python manage.py load_data_ingredients
docker compose exec backend python manage.py load_data_tags
```

**Готово!** Приложение доступно по адресу `http://localhost:8000`

## CI/CD Pipeline

Проект настроен на автоматический деплой через GitHub Actions. При каждом push в ветку `main`:

### Этап 1: Контроль качества
- **Тестирование** - запуск Django unit tests
- **Линтинг** - проверка кода с flake8
- **Проверка зависимостей** - анализ requirements.txt

### Этап 2: Сборка и публикация
Создание и публикация образов в Docker Hub:
- `yourusername/foodgram_backend:latest`
- `yourusername/foodgram_frontend:latest`
- `yourusername/foodgram_gateway:latest`

### Этап 3: Деплой
- Подключение к продакшн серверу по SSH
- Обновление docker-compose.production.yml
- Перезапуск контейнеров с новыми образами
- Выполнение миграций и сбор статики
- Очистка неиспользуемых Docker образов

### Этап 4: Уведомления
Отправка сообщения в Telegram об успешном деплое

## Настройка продакшн деплоя

### GitHub Secrets
Добавьте следующие секреты в настройки репозитория:

```
DOCKER_USERNAME      # Логин Docker Hub
DOCKER_PASSWORD      # Пароль Docker Hub  
HOST                 # IP адрес продакшн сервера
USER                 # Пользователь на сервере
SSH_KEY              # Приватный SSH ключ
PASSPHRASE           # Пароль SSH ключа (опционально)
TELEGRAM_TO          # ID чата Telegram
TELEGRAM_TOKEN       # Токен Telegram бота

# Переменные окружения для продакшена
DB_ENGINE            # django.db.backends.postgresql
DB_NAME              # Имя базы данных
DB_USER              # Пользователь БД
DB_PASSWORD          # Пароль БД
DB_HOST              # Хост БД (обычно db)
DB_PORT              # Порт БД (обычно 5432)
SECRET_KEY           # Секретный ключ Django
```

### Подготовка сервера
1. **Установите Docker и Docker Compose:**
```bash
sudo apt update
sudo apt install docker.io docker-compose
```

2. **Настройте файлы конфигурации:**
```bash
# Скопируйте файлы на сервер
scp docker-compose.production.yml user@server:/home/user/
scp nginx.conf user@server:/home/user/
```

3. **Создайте .env файл на сервере** с продакшн настройками

## API Documentation

### Аутентификация
```
POST /api/users/                    # Регистрация пользователя
POST /api/auth/token/login/         # Получение токена
POST /api/auth/token/logout/        # Выход из системы
GET  /api/users/me/                 # Профиль текущего пользователя
```

### Рецепты
```
GET    /api/recipes/                # Список рецептов (с фильтрацией)
POST   /api/recipes/                # Создание нового рецепта
GET    /api/recipes/{id}/           # Детали рецепта
PUT    /api/recipes/{id}/           # Обновление рецепта
DELETE /api/recipes/{id}/           # Удаление рецепта
GET    /api/recipes/download_shopping_cart/  # Скачать список покупок
```

### Избранное и список покупок
```
POST   /api/recipes/{id}/favorite/        # Добавить в избранное
DELETE /api/recipes/{id}/favorite/        # Удалить из избранного
POST   /api/recipes/{id}/shopping_cart/   # Добавить в список покупок
DELETE /api/recipes/{id}/shopping_cart/   # Удалить из списка покупок
```

### Подписки
```
GET    /api/users/subscriptions/    # Мои подписки
POST   /api/users/{id}/subscribe/   # Подписаться на пользователя
DELETE /api/users/{id}/subscribe/   # Отписаться от пользователя
```

### Ингредиенты и теги
```
GET /api/ingredients/               # Список ингредиентов
GET /api/ingredients/{id}/          # Информация об ингредиенте
GET /api/tags/                      # Список тегов
GET /api/tags/{id}/                 # Информация о теге
```

## Архитектура проекта

```
foodgram_final/
├── backend/                        # Django REST API
│   ├── foodgram/                   # Настройки проекта
│   ├── recipes/                    # Модели рецептов
│   ├── users/                      # Модели пользователей
│   ├── api/                        # API endpoints
│   ├── data/                       # Фикстуры (ингредиенты, теги)
│   ├── media/                      # Загружаемые файлы
│   ├── static/                     # Статические файлы
│   ├── requirements.txt            # Python зависимости
│   └── Dockerfile                  # Backend образ
│
├── frontend/                       # React приложение  
│   ├── src/                        # Исходники фронтенда
│   ├── build/                      # Собранный фронтенд
│   ├── package.json                # Node.js зависимости
│   └── Dockerfile                  # Frontend образ
│
├── nginx/                          # Веб-сервер
│   ├── nginx.conf                  # Конфигурация Nginx
│   └── Dockerfile                  # Gateway образ
│
├── docs/                           # Документация API
├── infra/                          # Инфраструктурные файлы
│   ├── docker-compose.yml          # Локальная разработка
│   └── docker-compose.production.yml  # Продакшн
├── .github/workflows/              # CI/CD
│   └── main.yml                    # GitHub Actions workflow
└── .env.example                    # Пример переменных окружения
```

## Особенности реализации

### Модели данных
- **User** - кастомная модель пользователя с дополнительными полями
- **Recipe** - рецепты с связями к ингредиентам и тегам
- **Ingredient** - ингредиенты с единицами измерения
- **Tag** - теги для категоризации рецептов
- **Follow** - подписки между пользователями
- **Favorite** - избранные рецепты пользователей
- **ShoppingCart** - корзина для формирования списка покупок

### API особенности
- Пагинация по умолчанию (PageNumberPagination)
- Фильтрация рецептов по тегам, автору, избранному
- Поиск ингредиентов по названию
- Кастомные permissions для CRUD операций
- Генерация PDF списка покупок

### Безопасность
- JWT аутентификация через Djoser
- Валидация данных на уровне сериализаторов
- Ограничения доступа через DRF permissions
- Санитизация загружаемых изображений

## Мониторинг и отладка

### Просмотр логов
```bash
# Все сервисы
docker compose logs -f

# Конкретный сервис
docker compose logs -f backend
docker compose logs -f frontend  
docker compose logs -f gateway
docker compose logs -f db
```

### Подключение к контейнерам
```bash
# Django shell
docker compose exec backend python manage.py shell

# Bash в backend контейнере
docker compose exec backend bash

# Подключение к PostgreSQL
docker compose exec db psql -U $DB_USER -d $DB_NAME
```

### Управление данными
```bash
# Создание дампа БД
docker compose exec db pg_dump -U $DB_USER $DB_NAME > backup.sql

# Восстановление из дампа
docker compose exec -T db psql -U $DB_USER -d $DB_NAME < backup.sql
```

## Тестирование

### Запуск тестов локально
```bash
# Все тесты
docker compose exec backend python manage.py test

# Конкретное приложение
docker compose exec backend python manage.py test recipes

# С coverage
docker compose exec backend coverage run --source='.' manage.py test
docker compose exec backend coverage report
```

## Результаты проекта

- **Живая демонстрация**: https://foodgram.kotpilota.ru/
- **Полнофункциональный REST API** с документацией
- **Современная архитектура** с разделением на микросервисы
- **Автоматизированный CI/CD** с полным циклом разработки
- **Контейнеризованное развертывание** готовое к продакшену
- **Социальные функции** - подписки, избранное, списки покупок

## Техническая документация

- **API docs**: доступна по адресу `/api/docs/` после запуска
- **Admin панель**: `/admin/` (требует суперпользователя)
- **Swagger UI**: интерактивная документация API
- **Redoc**: альтернативная документация API

---

<div align="center">

**Made with ❤️ for food lovers and cooking enthusiasts**

[⭐ Star this repo](https://github.com/yourusername/foodgram_final/stargazers) | [🐛 Report Bug](https://github.com/yourusername/foodgram_final/issues) | [💡 Request Feature](https://github.com/yourusername/foodgram_final/issues)

</div>
