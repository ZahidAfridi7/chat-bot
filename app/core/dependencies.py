from fastapi import Depends,HTTPException
from app.services.auth import get_current_user



async def require_subscription(tier: str, user: User = Depends(get_current_user)):
    if user.subscription_tier not in PREMIUM_TIERS[tier]:
        raise HTTPException(403, "Upgrade subscription for this feature")
    return user