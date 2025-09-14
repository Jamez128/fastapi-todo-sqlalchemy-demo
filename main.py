from fastapi import FastAPI, HTTPException, Depends
from typing import List
from db import Base, engine
from sqlalchemy.orm import Session
from db import SessionLocal
import models_db
import schemas


Base.metadata.create_all(bind=engine)

# ---- Create SQL Lite DB instance ----
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---- Create FastAPI APP instance ---- 
app = FastAPI(
    title="Users & Todos API",
    description="A demo REST API built with FastAPI to practice CRUD operations, REST principles, and auto-docs via Swagger UI",
    version="1.0.0"
)

# ---- User Routes ----
@app.post("/users", response_model=schemas.UserOut, summary="Create a user")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    db_user = db.query(models_db.User).filter(models_db.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create a new user in DB
    new_user = models_db.User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user # SQLAlchemy object -> auto-converted via UserOut

@app.get("/users", response_model=List[schemas.UserOut], summary="List all users")
def get_users(db: Session = Depends(get_db)):
    return db.query(models_db.User).all()

@app.get("/users/{user_id}", response_model=schemas.UserOut, summary="Get a user by ID")
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models_db.User).filter(models_db.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# ---- Todo Routes ----
@app.post("/users/{user_id}/todos", response_model=schemas.TodoOut, summary="Add a todo for a user")
def create_todo(user_id: int, todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    db_user = db.query(models_db.User).filter(models_db.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    new_todo = models_db.Todo(**todo.dict(), owner_id=user_id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@app.get("/users/{user_id}/todos", response_model=List[schemas.TodoOut], summary="List all todos for a user")
def get_user_todos(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models_db.User).filter(models_db.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db.query(models_db.Todo).filter(models_db.Todo.owner_id == user_id).all()

@app.get("/users/{user_id}/todos/{todo_id}", response_model=schemas.TodoOut, summary="Get a specific todo")
def get_todo(user_id: int, todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(models_db.Todo).filter(
        models_db.Todo.id == todo_id,
        models_db.Todo.owner_id == user_id
    ).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@app.put("/users/{user_id}/todos/{todo_id}", response_model=schemas.TodoOut, summary="Replace a todo")
def update_todo(user_id: int, todo_id: int, todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    db_todo = db.query(models_db.Todo).filter(
        models_db.Todo.id == todo_id,
        models_db.Todo.owner_id == user_id
    ).first()
    if not db_todo:
        raise HTTPException(status_code=404, details="Todo not found")
    for field, value in todo.dict().items():
        setattr(db_todo, field, value)
    
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.patch("/users/{user_id}/todos/{todo_id}", response_model=schemas.TodoOut, summary="Partially update a todo")
def patch_todo(user_id: int, todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(models_db.Todo).filter(
        models_db.Todo.id == todo_id,
        models_db.Todo.owner_id == user_id
    ).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    update_data = todo.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)

    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/users/{user_id}/todos/{todo_id}", summary="Delete a todo")
def delete_todo(user_id: int, todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(models_db.Todo).filter(
        models_db.Todo.id == todo_id,
        models_db.Todo.owner_id == user_id
    ).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(db_todo)
    db.commit()
    return {"message": f"Todo {todo_id} deleted for user {user_id}"}

