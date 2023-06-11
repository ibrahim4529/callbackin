from pydantic import BaseModel, UUID4
from typing import Optional


class _CallbackBase(BaseModel):
    name: str
    description: Optional[str]


class CallbackCreate(_CallbackBase):
    pass


class CallbackRead(_CallbackBase):
    id: int
    user_id: int
    is_running: bool
    path: UUID4
