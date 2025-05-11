from sqlalchemy import Column, ForeignKey, DateTime, Float, Integer, JSON, String
from app.db.base import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class InteractionHeatmap(Base):
    """Stores granular interaction data for heatmap visualization"""
    __tablename__ = "interaction_heatmaps"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Engagement Metrics
    message_length = Column(Integer)  # Characters
    response_time = Column(Float)     # Seconds
    interaction_duration = Column(Float)
    
    # Sentiment Analysis
    sentiment_score = Column(Float)   # -1 (negative) to 1 (positive)
    emotion = Column(String(20))      # happy/angry/sad/neutral
    
    # Derived Metrics
    engagement_score = Column(Float)  # 0-1 composite score
    cognitive_load = Column(Float)    # Estimated mental effort
    user = relationship("User", back_populates="heatmap_data")

class UserHeatmapProfile(Base):
    """Aggregated heatmap statistics for quick access"""
    __tablename__ = "user_heatmap_profiles"
    
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    last_updated = Column(DateTime)
    
    # Time-based aggregates
    peak_hours = Column(JSON)         # {"hour": 14, "score": 0.87}
    weekly_pattern = Column(JSON)     # {"monday": 0.76, ...}
    
    # Behavioral Averages
    avg_sentiment = Column(Float)
    avg_response_time = Column(Float)
    engagement_trend = Column(Float)  # Slope of last 7 days
    user = relationship("User", back_populates="heatmap_profile", uselist=False)