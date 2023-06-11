from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    """User model
    store all related github user information
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    login: str = Field(default=None)
    email: Optional[str] = Field(default=None, unique=True)
    name: str = Field(default=None)
    github_id: str = Field(default=None, unique=True)