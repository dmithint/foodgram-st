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


## Запуск проекта на удаленном сервере

1. Установить docker compose на сервер:
```bash
sudo apt update
```
```bash
sudo apt install curl
```
```bash
curl -fSL https://get.docker.com -o get-docker.sh
```
```bash
sudo sh ./get-docker.sh
```
```bash    
sudo apt-get install docker-compose-plugin
```

2. Скачать файл [prod-compose.yml](https://github.com/dmithint/foodgram-st/blob/main/prod-compose.production.yml) на сервер.

3. На сервере в директории с файлом **docker-compose.production.yml** создать файл  **.env** (см. .env_example):

4. Запустить Docker compose:
``` bash
sudo docker compose -f prod-compose.yml up -d
```

## Автор проекта [**Дмитрий Крыжановский**](https://github.com/dmithint)
