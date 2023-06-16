from sqlmodel import SQLModel, Field
from typing import Optional
import uuid

def get_uuid():
    return uuid.uuid4().__str__()

class Callback(SQLModel, table=True):
    """Cllback model
    store all callback information for each user
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    description: Optional[str] = Field(default=None)
    path: str = Field(unique=True, default_factory=get_uuid)
    local_endpoint: str = Field(nullable=False, default="http://localhost:8000/callbacks/1")
    user_id: int = Field(default=None, foreign_key="user.id")
    is_running: bool = Field(default=False)