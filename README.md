Установка: 1 - Клонирование репозитория 'gitclone (https://github.com/OldSumerian/SPA_DRF.git)'

2 - Установите необходимые зависимости, указанные в файле pyproject.toml ('poetry install')

3 - Заполнить данные в файле '.env' согласно списку из 'env.sample'

4 - Запустить Redis: 'redis-server'

5 - Настройка базы данных, примените миграции для настройки базы данных: 'python manage.py migrate'

6 - Запуск сервера разработки: 'python manage.py runserver'

7 - В терминале запустите:

celery worker: 'celery -A config worker -l INFO' или для Windows: 'celery -A config worker -l INFO -P eventlet' celery beat : ' celery -A config beat -l INFO'

Для запуска файла в Docker необходимо ввести команду в терминал:

docker-compose up -d --build
