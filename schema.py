from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    name: str

class ProductCreate(BaseModel):
    name: str
    price: float

class CartCreate(BaseModel):
    user_id: int
    product_ids: list[int] = Field(default_factory=list)

class CartContent(BaseModel):
    cart_id: int
    products: list[ProductCreate] = []