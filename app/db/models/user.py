from sqlalchemy import Column, Integer, String, Boolean, DateTime, func,JSON
from app.db.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    subscription_tier = Column(String(20), default='free')  # free/teaser+/premium/etc.
    quantum_access = Column(Boolean, default=False)
    heatmap_preferences = Column(JSON, default={
        "sensitivity": 0.7,
        "visible": True
    })
    voice_enabled = Column(Boolean, default=False)
    personality_matrix = Column(JSON, default={
        "empathy": 0.5,
        "humor": 0.3,
        "formality": 0.6
    })
    heatmap_data = relationship(
        "InteractionHeatmap", 
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    
    heatmap_profile = relationship(
        "UserHeatmapProfile",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False
    )
