# Task Manager API (Django + Django REST Framework)

A REST API with token authentication. Users can register, log in, and manage
their own tasks (create, read, update, delete). Data is stored in a SQLite database.

**Tech stack:** Python, Django, Django REST Framework, SQLite, Postman

## Setup (Windows, VS Code terminal)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Server runs at http://127.0.0.1:8000/

(Mac/Linux: activate with `source venv/bin/activate`)

## API Endpoints

| Method | Endpoint | Auth needed | Purpose |
|---|---|---|---|
| POST | /api/register/ | No | Create a user, returns token |
| POST | /api/login/ | No | Returns token |
| POST | /api/logout/ | Yes | Deletes token |
| GET | /api/tasks/ | Yes | List my tasks |
| POST | /api/tasks/ | Yes | Create a task |
| GET | /api/tasks/<id>/ | Yes | Get one task |
| PUT | /api/tasks/<id>/ | Yes | Update a task (all fields) |
| PATCH | /api/tasks/<id>/ | Yes | Update some fields |
| DELETE | /api/tasks/<id>/ | Yes | Delete a task |

Send the token in the header: `Authorization: Token <your_token>`

## Sample requests (JSON body)

Register / Login:
```json
{ "username": "hetvi", "password": "hetvi@123" }
```
Create task:
```json
{ "title": "Learn Django", "description": "Finish DRF basics", "is_completed": false }
```

## Run automated tests

```bash
python manage.py test
```

## Admin panel

```bash
python manage.py createsuperuser
```
Open http://127.0.0.1:8000/admin/ to see users and tasks stored in the database.
