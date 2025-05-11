import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.heatmap import InteractionHeatmap, UserHeatmapProfile
from app.db.models.chat import Message
from sqlalchemy import select

class HeatmapEngine:
    def __init__(self):
        # Configuration (adjust based on PDF requirements)
        self.engagement_weights = {
            'message_length': 0.3,
            'response_time': 0.4,
            'sentiment': 0.3
        }
    
    async def record_interaction(
        self,
        db: AsyncSession,
        user_id: int,
        user_message: str,
        ai_response: str,
        response_time: float
    ) -> InteractionHeatmap:
        """Log a new interaction with calculated metrics"""
        
        # Calculate metrics
        sentiment = await self._analyze_sentiment(user_message)
        engagement = self._calculate_engagement(
            message_length=len(user_message),
            response_time=response_time,
            sentiment=sentiment
        )
        
        # Create heatmap entry
        heatmap = InteractionHeatmap(
            user_id=user_id,
            message_length=len(user_message),
            response_time=response_time,
            sentiment_score=sentiment,
            engagement_score=engagement,
            cognitive_load=self._estimate_cognitive_load(ai_response)
        )
        
        db.add(heatmap)
        await self._update_user_profile(db, user_id)
        return heatmap
    
    async def _update_user_profile(self, db: AsyncSession, user_id: int):
        """Update aggregated user profile"""
        # Get last 30 days of data
        interactions = await db.execute(
            select(InteractionHeatmap)
            .where(InteractionHeatmap.user_id == user_id)
            .where(InteractionHeatmap.timestamp >= datetime.utcnow() - timedelta(days=30))
        )
        interactions = interactions.scalars().all()
        
        if interactions:
            profile = await db.get(UserHeatmapProfile, user_id) or \
                     UserHeatmapProfile(user_id=user_id)
            
            # Calculate time-based patterns
            hourly = self._calculate_hourly_pattern(interactions)
            weekly = self._calculate_weekly_pattern(interactions)
            
            # Update profile
            profile.peak_hours = hourly
            profile.weekly_pattern = weekly
            profile.avg_sentiment = np.mean([i.sentiment_score for i in interactions])
            profile.avg_response_time = np.mean([i.response_time for i in interactions])
            profile.last_updated = datetime.utcnow()
            
            db.add(profile)
    
    def _calculate_engagement(self, **metrics) -> float:
        """Composite engagement score (0-1)"""
        # Normalize metrics
        norm_length = min(metrics['message_length'] / 500, 1.0)
        norm_sentiment = (metrics['sentiment'] + 1) / 2  # Convert -1..1 to 0..1
        norm_response = 1 - min(metrics['response_time'] / 10, 1.0)
        
        # Weighted sum
        return (
            self.engagement_weights['message_length'] * norm_length +
            self.engagement_weights['response_time'] * norm_response +
            self.engagement_weights['sentiment'] * norm_sentiment
        )
    
    async def _analyze_sentiment(self, text: str) -> float:
        """Replace with actual sentiment analysis model"""
        # Mock implementation - integrate your PDF's VADER/TextBlob here
        return np.clip(len(text) / 200 - 0.5, -1, 1)  # Simple length-based mock
    
    def _estimate_cognitive_load(self, response: str) -> float:
        """Estimate mental effort required (0-1)"""
        word_count = len(response.split())
        return min(word_count / 100, 1.0)
    
    def _calculate_hourly_pattern(self, interactions: list) -> dict:
        """Identify peak engagement hours"""
        hours = [i.timestamp.hour for i in interactions]
        if hours:
            peak_hour = max(set(hours), key=hours.count)
            return {
                "hour": peak_hour,
                "score": hours.count(peak_hour) / len(hours)
            }
        return {}
    
    def _calculate_weekly_pattern(self, interactions: list) -> dict:
        """Weekly engagement trends"""
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        counts = {day: 0 for day in weekdays}
        
        for i in interactions:
            weekday = i.timestamp.weekday()
            counts[weekdays[weekday]] += 1
        
        total = max(1, len(interactions))
        return {day: counts[day]/total for day in weekdays}
    

heatmap_engine = HeatmapEngine()