from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, sessionmaker
from database import engine, User, Product, Cart
from database import get_db
from schema import UserCreate, ProductCreate, CartCreate


user_router = APIRouter()


@user_router.post("/users/{user_name}", response_model=UserCreate, tags=['user'])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@user_router.put("/users/{user_id}", response_model=UserCreate, tags=['user'])
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    db_user.name = user.name
    db.commit()
    db.refresh(db_user)
    return db_user

@user_router.delete("/users/{user_id}", tags=['user'])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return {"message": "Тебя больше не существует"}

#Эндпоинты для продуктов