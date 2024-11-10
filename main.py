from fastapi import FastAPI
from routers.routers_person import user_router
from routers.routers_cart import cart_router
from routers.routers_product import product_router
import uvicorn

app = FastAPI()
app.include_router(user_router)
app.include_router(product_router)
app.include_router(cart_router)


@app.get('/')
def hello():
    return {"message" : "switch to /docs"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    