from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from database import engine, User, Product, Cart
from database import get_db
from schema import UserCreate, ProductCreate, CartCreate

product_router = APIRouter()


@product_router.post("/products", response_model=ProductCreate, tags=['products'])
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(name=product.name, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

#Удаляю его
@product_router.delete("/products/{product_id}", tags=['products'])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    db.delete(db_product)
    db.commit()
    return {"message": "Галя! Отмена"}