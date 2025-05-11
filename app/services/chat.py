from datetime import datetime
from app.services.heatmap import heatmap_engine
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import ai_services

class ChatService:
    async def process_message(
        self,
        db: AsyncSession,
        user_id: int,
        message: str
    ) -> dict:
        start_time = datetime.now()
        
        # Generate AI response (your existing logic)
        response = await ai_services.generate_response(message)
        
        # Calculate response time
        response_time = (datetime.now() - start_time).total_seconds()
        
        # Record heatmap data
        await heatmap_engine.record_interaction(
            db=db,
            user_id=user_id,
            user_message=message,
            ai_response=response,
            response_time=response_time
        )
        
        return {
            "response": response,
            "engagement_score": heatmap_engine.last_engagement_score,
            "heatmap_available": True
        }