from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from database import engine, User, Product, Cart
from database import get_db
from schema import UserCreate, ProductCreate, CartCreate

cart_router = APIRouter()

#Эндпоинты корзины
#Создаю корзинку
@cart_router.post("/carts", response_model=CartCreate, tags=['cart'])
def create_cart(cart: CartCreate, db: Session = Depends(get_db)):
    db_cart = Cart(user_id=cart.user_id, products=",".join(map(str, cart.product_ids)))
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

#Добавляю продукты

@cart_router.post("/carts/{cart_id}/add_product", tags=['cart'])
def add_product_to_cart(cart_id: int, product_id: int, db: Session = Depends(get_db)):
    db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
    product_ids = db_cart.products.split(",") if db_cart.products else []
    product_ids.append(str(product_id))
    db_cart.products = ",".join(product_ids)
    db.commit()
    db.refresh(db_cart)
    return {"message": "Продукт добавлен"}

#Связываю Юзера и Корзинку
@cart_router.post("/carts/{cart_id}/assign_user/{user_id}", tags=['cart'])
def assign_cart_to_user(cart_id: int, user_id: int, db: Session = Depends(get_db)):
    db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
    db_cart.user_id = user_id
    db.commit()
    db.refresh(db_cart)
    return {"message": "Корзина теперь твоя"}
#Удаляю продукт из корзины
@cart_router.delete("/carts/{cart_id}/remove_product/{product_id}", tags=['cart'])
def remove_product_from_cart(cart_id: int, product_id: int, db: Session = Depends(get_db)):
    db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
    product_ids = db_cart.products.split(",") if db_cart.products else []    
    product_ids.remove(str(product_id))
    db_cart.products = ",".join(product_ids)
    db.commit()
    db.refresh(db_cart)    
    return {"message": "Положил товар обратно"}

#Удаляю корзину
@cart_router.delete("/carts/{cart_id}", tags=['cart'])
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
    db.delete(db_cart)
    db.commit()
    return {"message": "Корзинка удалена"}


#Эндпоинт для вывода юзера, его корзины и продуктов
@cart_router.get("/users/{user_id}/cart/details", tags=['result'])
def get_user_cart_details(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if db_cart is None:
        raise HTTPException(status_code=404, detail="Cart not found for this user")
    product_ids = db_cart.products.split(",") if db_cart.products else []
    products = []
    for product_id in product_ids:
        db_product = db.query(Product).filter(Product.id == int(product_id)).first()
        if db_product:
            products.append({
                "id": db_product.id,
                "name": db_product.name,
                "price": db_product.price,
            })
    return {
        "user": {
            "id": db_user.id,
            "name": db_user.name
        },
        "cart": {
            "id": db_cart.id,
            "products": products
        }
    }
