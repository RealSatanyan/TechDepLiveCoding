from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, sessionmaker
from database import engine, User, Product, Cart
from schema import UserCreate, ProductCreate, CartCreate

api_router = APIRouter()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@api_router.get("/hello")
def hello():
    return {"name": "Привет мир"}

#Эндпоинты для пользователя
@api_router.post("/users", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@api_router.put("/users/{user_id}", response_model=UserCreate)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    db_user.name = user.name
    db.commit()
    db.refresh(db_user)
    return db_user

@api_router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return {"message": "Тебя больше не существует"}

#Эндпоинты для продуктов

#Созжаю продукт
@api_router.post("/products", response_model=ProductCreate)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(name=product.name, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

#Удаляю его
@api_router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    db.delete(db_product)
    db.commit()
    return {"message": "Галя! Отмена"}

#Эндпоинты корзины
#Создаю корзинку
@api_router.post("/carts", response_model=CartCreate)
def create_cart(cart: CartCreate, db: Session = Depends(get_db)):
    db_cart = Cart(user_id=cart.user_id, products=",".join(map(str, cart.product_ids)))
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

#Добавляю продукты

@api_router.post("/carts/{cart_id}/add_product")
def add_product_to_cart(cart_id: int, product_id: int, db: Session = Depends(get_db)):
    db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
    product_ids = db_cart.products.split(",") if db_cart.products else []
    product_ids.append(str(product_id))
    db_cart.products = ",".join(product_ids)
    db.commit()
    db.refresh(db_cart)
    return {"message": "Продукт добавлен"}

#Связываю Юзера и Корзинку
@api_router.post("/carts/{cart_id}/assign_user/{user_id}")
def assign_cart_to_user(cart_id: int, user_id: int, db: Session = Depends(get_db)):
    db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
    db_cart.user_id = user_id
    db.commit()
    db.refresh(db_cart)
    return {"message": "Корзина теперь твоя"}
#Удаляю продукт из корзины
@api_router.delete("/carts/{cart_id}/remove_product/{product_id}")
def remove_product_from_cart(cart_id: int, product_id: int, db: Session = Depends(get_db)):
    db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
    product_ids = db_cart.products.split(",") if db_cart.products else []    
    product_ids.remove(str(product_id))
    db_cart.products = ",".join(product_ids)
    db.commit()
    db.refresh(db_cart)    
    return {"message": "Положил товар обратно"}

#Удаляю корзину
@api_router.delete("/carts/{cart_id}")
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
    db.delete(db_cart)
    db.commit()
    return {"message": "Корзинка удалена"}


#Эндпоинт для вывода юзера, его корзины и продуктов
@api_router.get("/users/{user_id}/cart/details")
def get_user_cart_details(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    db_cart = db.query(Cart).filter(Cart.user_id == user_id).first()
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