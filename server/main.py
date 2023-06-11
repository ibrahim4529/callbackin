from fastapi import FastAPI
from routers import auth_router, callback_router
from utils.db import create_db_and_tables

app = FastAPI()
app.include_router(auth_router)
app.include_router(callback_router)


@app.on_event("startup")
async def startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {
        "name": "Callbackin API",
        "version": "0.1.0",
        "description": "A simple API to manage callbacks",
        "author": "Ibrahim Hanif (ibrahim4529)",
        "github": "https://github.com/ibrahim4529/callbackin"
    }