### API-проект для сайта YAMDB:

Перед вами проект YAMDB (бэкенд)

Это сервис работает по сбору отзывов на различные произведения,
с возможностью сортировки контента по категориям и жанрам.
На каждый отзыв предусмотрена оценка по шкале от 0 до 10,
а также возможность комментарирования!

Благодаря этому коду вы сможете работать с контентом через API-запросы!

В проекте предусмотрена защита данных через JWT-токены,
а также предоставлен удобный функционал для работы администраторов!

### Примеры API-запросов:

РАБОТА С ПОЛЬЗОВАТЕЛЯМИ:

```
/api/v1/auth/signup/ - POST-запрос зарегистрирует юзера
/api/v1/auth/token/ - POST-запрос позволит получить токен
/api/v1/users/me/ - GET и PATCH запросы юзера для получения и изменения информации о себе
```

РАБОТА С ПРОИЗВЕДЕНИЯМИ (TITLE):

```
/api/v1/titles/ - GET и POST
/api/v1/titles/{title_id}/ - GET, PATCH, DELETE
```

РАБОТА С ЖАНРАМИ (GENRES):

```
/api/v1/genres/ - GET и POST
/api/v1/genres/{slug}/ - GET, PATCH, DELETE
```

РАБОТА С КАТЕГОРИЯМИ (CATEGORIES):

```
/api/v1/categories/ - GET и POST
/api/v1/categories/{slug}/ - GET, PATCH, DELETE
```

РАБОТА С ОТЗЫВАМИ (REVIEWS):

```
/api/v1/titles/{title_id}/reviews/ - GET и POST
/api/v1/titles/{title_id}/reviews/{reviews_id}/ - GET, PATCH, DELETE
```

РАБОТА С КОММЕНТАРИЯМИ (COMMENTS):

```
/api/v1/titles/{title_id}/reviews/{reviews_id}/comments/ - GET и POST
/api/v1/titles/{title_id}/reviews/{reviews_id}/comments/{comments_id}/ - GET, PATCH, DELETE
```

Документация с примерами запросов доступна тут: http://127.0.0.1:8000/redoc/

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/AllanKudi/api_yamdb
```

Перейти в директорию проекта:

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

Для Windows:

```
python -m venv env
source env/Scripts/activate
```

Для Linux и masOS:

```
python3 -m venv env
source env/bin/activate
```

Установить зависимости из файла requirements.txt через загрузчик pip:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py makemigrations
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

### Импорт данных из csv для наполнения базы:

Запустить команду импорта:

```
python manage.py baseimport
```

В терминале отобразится результат импорта.
Если какой-либо из файлов отсутствует, то он не будет импортирован.

Примеры файлов csv для наполнения базы находятся в папке reviews/static/data/*.csv:

```
    users.csv - файл для заполнения таблицы пользователей
    comments.csv - файл для заполнения таблицы комментариев к отзывам.
    titles.csv - файл для заполнения таблицы произведений.
    review.csv - файл для заполнения таблицы отзывов к произведениям.
    category.csv - файл для заполнения таблицы категорий произведений.
    genre.csv - файл для заполнения таблицы жанров произведений.
    genre_title.csv - файл для заполнения таблицы Many-to-Many: одно произведение может иметь несколько жанров.
```