from fastapi import FastAPI
from routers import auth_router, callback_router, handler_router
from utils.db import create_db_and_tables
from utils.mqtt import init_app
from fastapi.middleware.cors import CORSMiddleware


origins = [
    "http://localhost:5173",
    "https://callbackin.my.id"
]

app = FastAPI()
init_app(app)
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])
app.include_router(auth_router)
app.include_router(callback_router)
app.include_router(handler_router)


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