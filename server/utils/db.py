from sqlmodel import Session, SQLModel, create_engine, select
from utils.config import get_config
from models import *


config = get_config()
connect_args = {"check_same_thread": False}
engine = create_engine(config.DB_URL, echo=True, connect_args=connect_args)


def create_db_and_tables():
    """Create database and tables"""
    print("Creating database and tables...")
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get session if needed"""
    return Session(engine)