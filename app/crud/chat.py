from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.chat import Conversation, Message
from app.db.models.user import User
from datetime import datetime

class ConversationCRUD:
    async def get_conversation_history(
        self, 
        db: AsyncSession, 
        user_id: int,
        limit: int = 20
    ) -> list[Message]:
        """Get last N messages for a user"""
        result = await db.execute(
            select(Message)
            .join(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()

    async def store_interaction(
        self,
        db: AsyncSession,
        user_id: int,
        user_message: str,
        ai_response: str,
        sentiment_score: float
    ) -> tuple[Message, Message]:
        """Store a conversation interaction pair"""
        # Get or create active conversation
        conversation = await db.execute(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .where(Conversation.ended_at == None)
            .order_by(Conversation.started_at.desc())
        )
        conversation = conversation.scalar_one_or_none()
        
        if not conversation:
            conversation = Conversation(user_id=user_id)
            db.add(conversation)
            await db.commit()
            await db.refresh(conversation)
        
        # Store messages
        user_msg = Message(
            conversation_id=conversation.id,
            content=user_message,
            is_user=True,
            sentiment_score=sentiment_score
        )
        
        ai_msg = Message(
            conversation_id=conversation.id,
            content=ai_response,
            is_user=False,
            sentiment_score=None  # AI response sentiment can be analyzed later
        )
        
        db.add_all([user_msg, ai_msg])
        await db.commit()
        
        return user_msg, ai_msg

conversation_crud = ConversationCRUD()