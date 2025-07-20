from fastapi import FastAPI
from app.routes import users
from app.utils import auth_router

app = FastAPI()

app.include_router(users.router)
app.include_router(auth_router.router)
