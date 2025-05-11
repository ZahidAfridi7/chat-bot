from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, JSON,func
from app.db.base import Base

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    summary = Column(String(500), nullable=True)

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    content = Column(String(1000))
    is_user = Column(Boolean)
    sentiment_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    heatmap_metadata = Column(JSON)  # For engagement tracking