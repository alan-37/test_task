# Платформа для обмена вещами между пользователями.
Пользователи могут:

- Создавать объявления о товарах.
- Искать и фильтровать объявления.
- Отправлять предложения об обмене.
- Управлять своим профилем и предложениями.

# Установка и запуск
1. Клонируй репозиторий:
    - git clone https://github.com/yourusername/barter-platform.git
    - cd barter-platform
3.  Создай виртуальное окружение и активируй его:
    - python -m venv venv
    - source venv/bin/activate    # Linux/Mac
    - venv\Scripts\activate       # Windows
4. Установи зависимости:
    - pip install -r requirements.txt

# Настройка проекта
1. Выполни миграции:
   - python manage.py makemigrations
   - python manage.py migrate

2. Создай суперпользователя (админ):
   - python manage.py createsuperuser
  
# Запуск сервера
- python manage.py runserver
- Открой в браузере: http://localhost:8000/

# Основные маршруты
- / - Главная страница со всеми обявлениями
- /ads/create/ - Создание объявления
- /ads/<int:pk>/edit/ - Редактирование объявления
- /ads/<int:pk>/delete/ - Удаление объявления
- /proposals/send/<int:ad_receiver_id>/ - Отправка предложения обмена
- /signup/ - Регистрация
- /login/ - Авторизация
- /logout/ - Выход из аккаунта
- /profile/ - Личный профиль пользователя с заявками и объявлениями
- /proposal/<int:proposal_id>/accept/ - Принять предложение
- /proposal/<int:proposal_id>/reject/ - Отклонить предложение
- /admin/ - Панель администратора

# Тестирование
Запуск тестов: python manage.py test

Тесты находятся в ads/tests.py
