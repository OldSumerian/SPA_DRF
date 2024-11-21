# SPA-DRF-приложение "Трекер полезных привычек"

## Описание проекта:
Бэкенд часть SPA-DRF-веб-приложения, предусматривающая интеграцию с Телеграмм-ботом
(реализованы модели полезных привычек и системы вознаграждений за их выполнение путем периодических задач)

## Стек проекта:
Python 3+, Django, DRF, PostgreSQL, Redis, Celery, Docker и т.д. (подробно в файле зависимостей *pyproject.toml*)


## Установка: 
1 - Клонирование репозитория 'gitclone (https://github.com/OldSumerian/SPA_DRF.git)'

2 - Установите необходимые зависимости, указанные в файле _pyproject.toml_ ('_poetry install_')

3 - Заполнить данные в файле '.env' согласно списку из 'env.sample'

4 - Запустить Redis: '_redis-server_'

5 - Настройка базы данных, примените миграции для настройки базы данных: '_python manage.py migrate_'

6 - Запуск сервера разработки: '_python manage.py runserver_'

7 - В терминале запустите:

_celery worker: 'celery -A config worker -l INFO' или для Windows: 'celery -A config worker -l INFO -P eventlet' celery beat : ' celery -A config beat -l INFO'_

Для запуска файла в Docker необходимо ввести команду в терминал:

_docker-compose up -d --build_
