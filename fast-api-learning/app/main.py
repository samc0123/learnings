from fastapi import FastAPI
from routers import users
import uvicorn


app = FastAPI()

app.include_router(users.router)


if __name__ == "__main__":
    uvicorn.run("main:app",host='localhost', port=8000)