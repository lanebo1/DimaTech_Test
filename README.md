# Тестовое задание для стажировки в команду разработки DimaTech Ltd

## Задача

https://docs.google.com/document/d/1-fvs0LaX2oWPjO6w6Bpglz1Ndy_KrNV7NeNgRlks94k/edit?tab=t.0#heading=h.kjndgn4egzox

## Решение

### Используемые технологии

- FastAPI - фреймворк для создания API на Python
- SQLAlchemy - ORM для работы с базой данных
- PostgreSQL - СУБД
- Docker - контейнеризация приложения
- Pydantic - валидация данных
- PyJWT - работа с JWT-токенами

### Структура проекта

- `auth\auth_ops.py` - функции для работы с авторизацией
- `database\`
    - `crud.py` - функции для работы с базой данных
    - `models.py` - модели таблиц базы данных
    - `schemas.py` - схемы для валидации данных
    - `database.py` - настройка и инициализация базы данных
- `routes\`
    - `admin.py` - маршруты для администратора
    - `users.py` - маршруты для пользователей
    - `routes.py` - общие маршруты (для отладки)
    - `webhooks.py` - маршруты для вебхуков
- `main.py` - основной файл приложения
- `Dockerfile, docker-compose.yml, .dockerignore` - файлы для сборки и конфигурации образа Docker
- `requirements.txt` - список зависимостей
- `README.md` - описание проекта

### Запуск проекта локально

1. Склонировать репозиторий:

```bash
git clone https://github.com/lanebo1/DimaTech_Test.git
```

2. Перейти в папку проекта:

```bash
cd DimaTech_Test
```

3. Активировать виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate
```

4. Установить зависимости:

```bash
pip install -r requirements.txt
```

5. Запустить проект:

```bash
uvicorn main:app --reload
```

6. Перейти по адресу:

```commandline
http://localhost:8000/docs
```

7. Использовать Swagger для тестирования API

### Запуск проекта в Docker

1. Повтроить пункты 1-4 из предыдущего раздела
2. Собрать образ Docker:

```bash
docker build -t dimatech-test .
```

3. Запустить контейнер:

```bash
docker run -d --name dimatech-test -p 8000:8000 dimatech-test
```

4. Повторить пункты 6-7 из предыдущего раздела

### Примеры запросов

1. Регистрация обычного пользователя (``` /create_user ```)

```JSON
{
  "email": "user@example.com",
  "full_name": "user_name",
  "password": "user_password",
  "is_admin": false
}
```

2. Регистрация администратора (``` /create_user ```)

```JSON
{
  "email": "admin@example.com",
  "full_name": "admin_name",
  "password": "admin_password",
  "is_admin": true
}
```

3. Авторизация (``` ипользовать значок закрытого замка (Authorize) в Swagger ```):

   Заполнить поля username и password -> нажать Authorize -> пользователь авторизован
4. Создание вебхука (``` /generate-webhook ```)
    1. Создание транзакции генерируя новый счет пользователя:

       Заполнить поле user_id -> нажать Execute -> в ответе будет сгенерированный счет
    2. Создание транзакции в уже имеющийся счет пользователя:

       Заполнить поля user_id и user_account_id -> нажать Execute -> в ответе будет сгенерированный счет
5. Обработка вебхука (``` /webhook ```)

   Вставить в тело запроса вебхук созданный в пункте 4 -> нажать Execute -> в ответе будет обработанный вебхук
6. Проверка показателей пользвателя (``` /user/... ```) (доступно только обычному пользователю, для авторизации
   использовать пункт 3)

    1. Получение информации о пользователе (``` /user/me ```)
    2. Получение информации о всех аккаунтах (счетах) пользователя (``` /user/accounts ```)
    3. Получение информации о всех транзакциях пользователя (``` /user/payments ```)
7. Проверка показателей админа (``` /admin/... ```) (доступно только администратору, для авторизации использовать пункт 3)

    1. Получение информации о всех пользователях (``` GET /admin/users ```)
    2. Создание нового пользователя (``` POST /admin/users ```)
    3. Удаление пользователя (``` DELETE /admin/users/{user_id} ```)
    4. Изменение пользователя (``` PUT /admin/users/{user_id} ```)
    5. Получение информации о всех аккаунтах конкретного пользователя (``` GET /admin/users/{user_id}/accounts ```)


