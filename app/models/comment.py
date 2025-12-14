from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Commnent(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    post_id: str
    author: Optional[str] = None
    content: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)