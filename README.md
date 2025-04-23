[![Foodgram workflow status](https://github.com/dmithint/foodgram-st/actions/workflows/main.yml/badge.svg)](https://github.com/dmithint/foodgram-st/actions/workflows/main.yml)

# Проект: [Foodgram](http://194.87.69.242/)
### Дипломный проект *Яндекс.Практикум* курса Backend-разработчик(python)

Проект Foodgram дает возможность пользователям создавать и хранить рецепты на онлайн-платформе. Кроме того, можно скачать список продуктов, необходимых для приготовления блюда, просмотреть рецепты друзей и добавить любимые рецепты в список избранных.

## Технологии
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-092E20?style=for-the-badge&logo=django&logoColor=white)
![Djoser](https://img.shields.io/badge/Djoser-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

## [API документация](http://194.87.69.242/redoc/)

## [Администрирование](http://194.87.69.242/admin/)

    Email: admin@foodgram.ru
    Password: asdfasdf

## Запуск проекта (только backend)

### Требования
* Python 3.9+

1. Клонирование репозитория и переход в директорию проекта
``` bash
    git clone https://github.com/dmithint/foodgram-st.git
    cd foodgram-st/backend
```

2. Создание и активация виртуального окружения
``` bash
    python -m venv venv
    source venv/bin/activate  # Для Windows: venv\Scripts\activate
```

3. Установка зависимостей
``` bash
    pip install --upgrade pip
    pip install -r requirements.txt
```

4. Настройка переменных окружения (backend/.env)

* Необязательно, но см. **.env_example**

5. Применение миграций и загрузка данных
``` bash
    python manage.py migrate
    python manage.py load_ingredients
```

6. Сбор статических файлов
``` bash
    python manage.py collectstatic --noinput
```

7. Запуск проекта
``` bash
    python manage.py runserver
```

8. Открытие в браузере

* Сайт: http://127.0.0.1:8000
* Админка: http://127.0.0.1:8000/admin


## Запуск проекта локально

1. Описать файл infra/local/.env (см. .env_example)

2. Запустить Docker compose:
``` bash
sudo docker compose -f infra/local/docker-compose.yml up -d
```

## Запуск проекта на удаленном сервере

1. Установить docker compose на сервер

2. Скачать файл [prod-compose.yml](https://github.com/dmithint/foodgram-st/blob/main/infra/prod/prod-compose.yml) на сервер.

3. На сервере в директории с файлом **prod-compose.yml** создать файл  **.env** (см. .env_example):

4. Запустить Docker compose:
``` bash
sudo docker compose -f prod-compose.yml up -d
```

## Автор проекта [**Дмитрий Крыжановский**](https://github.com/dmithint)
