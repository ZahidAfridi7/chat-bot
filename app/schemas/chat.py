from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    is_user: bool
    
class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    created_at: datetime
    sentiment_score: Optional[float]
    
    class Config:
        from_attributes = True

class Conversation(BaseModel):
    messages: List[Message]
    heatmap_data: Optional[dict]