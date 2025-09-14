# FastAPI Users & Todos Demon (with SQLAlchemy + SQLite)

A demo REST API built with **FastAPI**, **SQLAlchemy ORM**, and **SQLite**.
This project demonstrates CRUD operations (Create, Read, Update, Delete) for a 'User' resource and their related 'Todos'.

---

## Features
- **Users**
    - Create a user ('POST /users')
    - List all users ('GET /users')
    - Get user by ID ('GET /users/{id}')

- **Todos**
    - Create a todo for a user ('POST /users/{id}/todos')
    - List all todos for a user ('GET /users/{id}/todos')
    - Get a todo by ID ('GET /users/{id}/todos/{todo_id}')
    - Replace a todo ('PUT /users/{id}/todos/{todo_id}')
    - Partially update a todo ('PATCH /ysers/{id}/todos/{todos_id}')
    - Delete a todo ('Delete /users/{id}/todos/{todo_id}')

---

## Installation

Clone this repo and install dependancies:

```bash
git clone <this repo>
cd fastapi-todo-sqlalchemy-demo
python -m venv .venv
source .venv/bin/activate # or .venv/Scripts/activate on Windows
pip install -r requirements.txt
```

Running the API
```
uvicorn main:app --reload
```

The API will be available at:
- http://127.0.0.1:8000
* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc

Example Requests:
- Create a User
```
POST /users
Content-Type: application/json

{
    "username": "alice",
    "email": "alice@example.com"
}
```

- Create a Todo for User 1
```
POST /users/1/todos
Content-Type: application/json

{
    "title": "Buy milk",
    "description": "2L carton",
    "done": false
}
```

Tech Stack utilised in demo:
* FastAPI - Web framework (provides HTTP server layer- routes, request handling, auto docs)
* SQLAlchemy - ORM (Object Relational Mapper, bridges between Python Objects and SQL tables, otherwise it'd be written in SQL, and keeps it easy for changing SQLite to Postgres later *just an example of why to use ORM*)
* SQLite - Lightweight database (A full relational DB, but file-based with no server needed, great for demos and small apps. If switching to Postgres/MySQL later, SQLAlchemy code mostly stays the same- only the connection string needs changing)
* Pydantic - Data validation (for example it will throw an error for us if the email: EmailStr doesn't contain the '@'...)

Notes:
* The SQLite database is stored in todos.db (auto-created on first run).
* This project is for learning/demo purposes. For production, swap SQLite for Postgres/MySQL and use Alembic for migrations.
