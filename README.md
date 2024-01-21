# Руководство по развертыванию

### Шаг 1: Получение исходного кода
 - Склонируйте репозиторий из GitHub:
 `https://github.com/ilin-art/spb_library_test.git`
 `cd EventHub`

 ### Шаг 2: Запуск Docker Compose
 - Выполните следующую команду для развертывания приложения с использованием Docker Compose:
 `docker-compose up -d`

 ### Шаг 3: Применение миграций Django
 - Запустите миграции Django для создания базы данных:
 `docker-compose exec web python manage.py migrate`

 ### Шаг 4: Создание суперпользователя
 - Создайте суперпользователя для управления административной частью приложения:
 `docker-compose exec web python manage.py createsuperuser`

 ### Шаг 5: Перезапуск Docker Compose
 - Перезапустите Docker Compose, чтобы применить изменения:
 `docker-compose down`
 `docker-compose up -d`

 ### Завершение
 - Теперь ваше приложение должно быть развернуто и доступно по адресу http://localhost:8000. Вы можете войти в административную панель с использованием учетных данных суперпользователя.