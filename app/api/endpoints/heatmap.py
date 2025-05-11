from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal
from datetime import timedelta,datetime
from app.services.auth import get_current_user
from app.db.session import get_db
from app.services.heatmap import heatmap_engine
from app.db.models.user import User
from app.db.models.heatmap import InteractionHeatmap,UserHeatmapProfile
from sqlalchemy import select

router = APIRouter()

@router.get("/raw")
async def get_raw_heatmap(
    timeframe: Literal['24h', '7d', '30d'] = '7d',
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get raw heatmap data for visualization"""
    time_ago = {
        '24h': timedelta(hours=24),
        '7d': timedelta(days=7),
        '30d': timedelta(days=30)
    }[timeframe]
    
    result = await db.execute(
        select(InteractionHeatmap)
        .where(InteractionHeatmap.user_id == current_user.id)
        .where(InteractionHeatmap.timestamp >= datetime.utcnow() - time_ago)
        .order_by(InteractionHeatmap.timestamp)
    )
    
    interactions = result.scalars().all()
    
    return JSONResponse(content={
        "timestamps": [i.timestamp.isoformat() for i in interactions],
        "engagement": [i.engagement_score for i in interactions],
        "sentiment": [i.sentiment_score for i in interactions],
        "response_times": [i.response_time for i in interactions]
    })

@router.get("/summary")
async def get_heatmap_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get aggregated heatmap insights"""
    profile = await db.get(UserHeatmapProfile, current_user.id)
    
    if not profile:
        raise HTTPException(404, "No heatmap data available")
    
    return {
        "peak_engagement": profile.peak_hours,
        "weekly_pattern": profile.weekly_pattern,
        "average_sentiment": profile.avg_sentiment,
        "engagement_trend": profile.engagement_trend,
        "last_updated": profile.last_updated.isoformat()
    }


#@router.get("/user/{user_id}")
#async def get_full_heatmap(
#    user_id: int,
#    db: AsyncSession = Depends(get_db),
#    admin: User = Depends(get_current_user)
#):
#    """For admin dashboard - shows complete heatmap relationship"""
#    user = await db.get(User, user_id, options=[
#        selectinload(User.heatmap_data.order_by(InteractionHeatmap.timestamp.desc()).limit(1000),
#        selectinload(User.heatmap_profile)
#    ])
#    
#    if not user:
#       raise HTTPException(404, "User not found")
    
#    return {
#        "user": user,
#        "heatmap_stats": user.heatmap_profile,
#        "recent_interactions": user.heatmap_data
#    }
        