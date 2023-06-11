from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class CallbackHistory(SQLModel, table=True):
    """CallbackHistory model
    store all callback history information
    this history will be used to re forward the request and logging
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    callback_id: str = Field(foreign_key="callback.id")
    timestamp: datetime = Field(default=None)
    headers: str = Field(default=None)
    body: str = Field(default=None)