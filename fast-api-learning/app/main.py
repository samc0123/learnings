from fastapi import FastAPI
from routers import users, transactions, products
import uvicorn


app = FastAPI()

app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(products.router)


if __name__ == "__main__":
    uvicorn.run("main:app",host='localhost', port=8000)