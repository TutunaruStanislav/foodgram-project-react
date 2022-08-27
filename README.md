# foodgram-project-react

![example workflow](https://github.com/TutunaruStanislav/foodgram-project-react/actions/workflows/main.yml/badge.svg)

### Описание:
Foodgram - продуктовый помощник, поможет облегчить подсчет ингредиентов 
для выбранных блюд.

Ниже приведены основные возможности сервиса:
* Отображение общего списка рецептов, с возможностью фильтрации по тегам
* Просмотр карточки рецепта
* Добавление рецепта в избранное
* Подписка на автора рецептов
* Регистрация в системе
* Создание своего рецепта
* Добавление рецептов в список и загрузка файла со сводной информацией

### Стек технологий:
Python 3.7

Django 2.2.16

Postgres 13.0

React
### Как собрать и запустить проект:

Клонировать репозиторий:

```
git clone https://github.com/TutunaruStanislav/foodgram-project-react.git
```

Скопировать .env.example в .env и заполнить его:

```
cp .env.example ./infra/.env
```

Перейти в папку infra, собрать и запустить контейнеры:

```
cd infra
```

```
docker-compose up -d --build
```
Последовательно выполнить команды:

```
docker-compose exec web python manage.py migrate
```

```
docker-compose exec web python manage.py loaddata fixtures.json
```

```
docker-compose exec web python manage.py collectstatic --no-input
```

```
docker-compose exec web python manage.py createsuperuser
```

Проект будет доступен по следующему адресу:

http://localhost/

### Запросы / ответы:

* http://localhost/admin/ - панель администратора
* GET http://localhost/api/users/?page=2&limit=2 - список всех пользователей, с пагинацией
```
HTTP Statuses: 200
```
```json lines
Response body
{
    "count": 6,
    "next": "http://127.0.0.1:8000/api/users/?limit=2&page=3",
    "previous": "http://127.0.0.1:8000/api/users/?limit=2",
    "results": [
        {
            "email": "user2@mail.com",
            "id": 4,
            "username": "user2",
            "first_name": "Ирина",
            "last_name": "К",
            "is_subscribed": false
        },
        {
            "email": "user3@mail.com",
            "id": 6,
            "username": "user3",
            "first_name": "Анжелика",
            "last_name": "И",
            "is_subscribed": false
        }
    ]
}
```

* POST http://localhost/api/users/ - добавить нового пользователя

```json lines
Request Body
{
    "username": "user8",
    "email": "user8@mail.com",
    "first_name": "Валентина",
    "last_name": "А",
    "password": "********"
}
```
```
HTTP Statuses: 201, 400
```

* GET http://localhost/api/recipes/?page=1&limit=1 - список рецептов

```
HTTP Statuses: 200
```
```json lines
Response body
{
    "count": 5,
    "next": "http://127.0.0.1:8000/api/recipes/?limit=1&page=2",
    "previous": null,
    "results": [
        {
            "id": 12,
            "tags": [
                {
                    "id": 2,
                    "name": "Обед",
                    "color": "#FFAE3A",
                    "slug": "dinner"
                },
                {
                    "id": 3,
                    "name": "Ужин",
                    "color": "#E53209",
                    "slug": "evening-meal"
                }
            ],
            "author": {
                "email": "user3@mail.com",
                "id": 6,
                "username": "user3",
                "first_name": "Анжелика",
                "last_name": "И",
                "is_subscribed": false
            },
            "ingredients": [
                {
                    "id": 1285,
                    "name": "перец черный молотый",
                    "measurement_unit": "г",
                    "amount": 3
                },
                {
                    "id": 1685,
                    "name": "соль",
                    "measurement_unit": "г",
                    "amount": 3
                },
                {
                    "id": 252,
                    "name": "вода",
                    "measurement_unit": "г",
                    "amount": 600
                },
                {
                    "id": 1420,
                    "name": "растительное масло",
                    "measurement_unit": "г",
                    "amount": 40
                },
                {
                    "id": 1205,
                    "name": "паприка красная молотая",
                    "measurement_unit": "г",
                    "amount": 20
                },
                {
                    "id": 1855,
                    "name": "томатная паста",
                    "measurement_unit": "г",
                    "amount": 30
                },
                {
                    "id": 886,
                    "name": "лук репчатый",
                    "measurement_unit": "г",
                    "amount": 850
                },
                {
                    "id": 278,
                    "name": "говядина",
                    "measurement_unit": "г",
                    "amount": 850
                }
            ],
            "is_favorited": false,
            "is_in_shopping_cart": false,
            "name": "Венский гуляш",
            "image": "http://127.0.0.1:8000/media/service/u-725db55deebb29c5ff02e461a06e87dc.jpg",
            "text": "Когда говорят про австрийскую кухню, отдельной строкой обычно выделяют кухню венскую. Этому имеется довольно простое объяснение: Вена являлась столицей огромной австро-венгерской империи с очень неоднородным национальным составом. И на кухню столицы оказали влияние кухни всех провинций. Поэтому она не совпадает ни с кухней современной Австрии, ни с кухней тех стран, которые образовались после распада Австро-Венгрии. Вот казалось бы, ну кто им там, в столице, мешал готовить нормальный гуляш по-венгерски? Так нет же, переиначили все на свой манер и тоже назвали гуляшом! Попробуйте найти теперь черты сходства...",
            "cooking_time": 285
        }
    ]
}
```

* GET http://localhost/api/recipes/7/ - получение информации о рецепте

```
Path parameters:
id: 7 (integer)
```
```
HTTP Statuses: 200, 404
```
```json lines
Response body
{
    "id": 12,
    "tags": [
        {
            "id": 2,
            "name": "Обед",
            "color": "#FFAE3A",
            "slug": "dinner"
        },
        {
            "id": 3,
            "name": "Ужин",
            "color": "#E53209",
            "slug": "evening-meal"
        }
    ],
    "author": {
        "email": "user3@mail.com",
        "id": 6,
        "username": "user3",
        "first_name": "Анжелика",
        "last_name": "И",
        "is_subscribed": false
    },
    "ingredients": [
        {
            "id": 1285,
            "name": "перец черный молотый",
            "measurement_unit": "г",
            "amount": 3
        },
        {
            "id": 1685,
            "name": "соль",
            "measurement_unit": "г",
            "amount": 3
        },
        {
            "id": 252,
            "name": "вода",
            "measurement_unit": "г",
            "amount": 600
        },
        {
            "id": 1420,
            "name": "растительное масло",
            "measurement_unit": "г",
            "amount": 40
        },
        {
            "id": 1205,
            "name": "паприка красная молотая",
            "measurement_unit": "г",
            "amount": 20
        },
        {
            "id": 1855,
            "name": "томатная паста",
            "measurement_unit": "г",
            "amount": 30
        },
        {
            "id": 886,
            "name": "лук репчатый",
            "measurement_unit": "г",
            "amount": 850
        },
        {
            "id": 278,
            "name": "говядина",
            "measurement_unit": "г",
            "amount": 850
        }
    ],
    "is_favorited": false,
    "is_in_shopping_cart": false,
    "name": "Венский гуляш",
    "image": "http://127.0.0.1:8000/media/service/u-725db55deebb29c5ff02e461a06e87dc.jpg",
    "text": "Когда говорят про австрийскую кухню, отдельной строкой обычно выделяют кухню венскую. Этому имеется довольно простое объяснение: Вена являлась столицей огромной австро-венгерской империи с очень неоднородным национальным составом. И на кухню столицы оказали влияние кухни всех провинций. Поэтому она не совпадает ни с кухней современной Австрии, ни с кухней тех стран, которые образовались после распада Австро-Венгрии. Вот казалось бы, ну кто им там, в столице, мешал готовить нормальный гуляш по-венгерски? Так нет же, переиначили все на свой манер и тоже назвали гуляшом! Попробуйте найти теперь черты сходства...",
    "cooking_time": 285
}
```

Более полная документация с описанием доступных запросов, ответов и статусов, расположена по адресу - http://localhost/api/docs/

#### Проект доступен по адресу: http://51.250.107.213
Доступ в админку: admin007 / aA123456789

### Авторы:
Stanislav Tutunaru

### Лицензия:

MIT