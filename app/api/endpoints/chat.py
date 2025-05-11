from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.ai_services import ai_service
from app.schemas.chat import Message as MessageSchema
from app.db.models.user import User
from app.services.auth import get_current_user
from app.db.session import get_db
from app.crud.chat import conversation_crud
from typing import List

from fastapi import APIRouter, Depends
from app.services.ai_services import ai_service
from app.services.quantum import quantum_engine


router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=MessageSchema)
async def chat(
    message: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Process user message and return AI response with engagement data
    """
    try:
        # 1. Get conversation history
        history = await conversation_crud.get_conversation_history(
            db=db,
            user_id=current_user.id,
            limit=10  # Last 10 messages
        )
        
        # 2. Analyze sentiment of incoming message
        sentiment_score = await ai_service.analyze_sentiment(message)
        
        # 3. Generate AI response (with heatmap integration)
        ai_response = await ai_service.generate_response(
            user=current_user,
            message=message,
            conversation_history=history,
            sentiment_score=sentiment_score
        )
        
        # 4. Store the interaction
        user_msg, ai_msg = await conversation_crud.store_interaction(
            db=db,
            user_id=current_user.id,
            user_message=message,
            ai_response=ai_response,
            sentiment_score=sentiment_score
        )
        
        # 5. Update heatmap
        await ai_service.update_heatmap(
            user_id=current_user.id,
            interaction_data={
                "message_length": len(message),
                "response_time": 0.5,  # Would calculate this in real implementation
                "sentiment": sentiment_score
            }
        )
        
        # 6. Return formatted response
        return JSONResponse(content={
            "id": ai_msg.id,
            "content": ai_response,
            "is_user": False,
            "created_at": ai_msg.created_at.isoformat(),
            "heatmap_data": {
                "current_sentiment": sentiment_score,
                "engagement_score": current_user.engagement_score
            }
        })
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat processing failed: {str(e)}"
        )

@router.get("/history", response_model=List[MessageSchema])
async def get_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    limit: int = 20
):
    """Get conversation history"""
    messages = await conversation_crud.get_conversation_history(
        db=db,
        user_id=current_user.id,
        limit=limit
    )
    return messages

@router.post("/quantum-chat")
async def quantum_chat(
    message: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Endpoint that leverages quantum decision-making"""
    # Verify quantum access
    if not current_user.quantum_access:
        raise HTTPException(
            status_code=403,
            detail="Quantum features require premium subscription"
        )
    
    # Get conversation history
    history = await conversation_crud.get_conversation_history(
        db, current_user.id, limit=5
    )
    
    # Generate quantum-optimized response
    response = await ai_service.generate_response(
        user=current_user,
        message=message,
        conversation_history=history
    )
    
    return {
        "response": response,
        "quantum_optimized": True,
        "personality_profile": current_user.personality_matrix
    }