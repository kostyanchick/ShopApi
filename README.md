## Simple shop api
(tested with python 3.7)
***
### Setup 

#### Python requirements

To start you need to have installed python 3.7

Firstly create virtual environments for project
And activate it

```
python3.7 -m venv venv
source /venv/bin/activate
```

install packages from requirements.txt located at root path:

``pip install requirements.txt``
***
#### Postgres setup
To run postgres in docker just run the command

``docker-compose up -d``

To stop

``docker-compose stop``

To clean up everything after usage

``docker-compose down -v --rmi all --remove-orphans``

To use local server please create database with name ``shop_dev`` or any other

``psql -c 'create database shop_dev;' ``

or run script initializing the whole db with all tables:
```
psql -f service_api/db/init_db.sql
```

and change in app config PG_PORT, PG_USER, PG_PW, PG_DB_NAME with actual values 
or export them as environment variables
***
### Run App
After db server ran we can start our application by running script:

``python run.py``

it will set up tables if they do not exist

***
### Api usage
db contains 4 tables:
- users - contains user entities
- categories - contains category entities
- user_category - association table to provide relationship many-to-many
between users and categories. 
Purpose is to give access to user to specific categories
- items - contains item entities with foreign key 
referencing to categories table
#### - Work with users:
(use postman or equivalent requests in curl)

get list of all users

``GET http://localhost:8080/shop_api/v1/users``

create new user

```
POST http://localhost:8080/shop_api/v1/users
body: {"usern_name": <user_name>}
```

get categories available for user

``GET http://localhost:8080/shop_api/v1/users/<user_id>/categories``

make category available for user 
(creates relationship in association table user_category)
```
POST http://localhost:8080/shop_api/v1/users/<user_id>/categories
body: {"category_id": <category_id>}
```

get items from categories available for user

``GET http://localhost:8080/shop_api/v1/users/<user_id>/items``

#### - Work with categories
get list of all categories

``GET http://localhost:8080/shop_api/v1/categories``

create new category

```
POST http://localhost:8080/shop_api/v1/categories
body: {"category_name": <category_name>}
```

get list of items for specific category
``GET http://localhost:8080/shop_api/v1/categories/<category_id>/items``


create new item for specific category

```
POST http://localhost:8080/shop_api/v1/categories/<category_id>/items
body: {"item_name": <items_name>}
```

#### - Work with items
get list of all items

``GET http://localhost:8080/shop_api/v1/items``

