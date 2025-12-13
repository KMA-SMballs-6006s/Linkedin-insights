from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Post(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    page_id: str
    content: str
    posted_at: datetime
    scraped_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True