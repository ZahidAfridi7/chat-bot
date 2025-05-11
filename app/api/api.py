from fastapi import APIRouter
from app.api.endpoints import (
    user,auth,chat,quantum,heatmap
)
       

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(auth.router, prefix="/auth", tags=["login"])
api_router.include_router(auth.router, prefix="/chat", tags=["Chat"])
api_router.include_router(auth.router, prefix="/quantum", tags=["Quantum Integration"])
api_router.include_router(auth.router, prefix="/heatmap", tags=["heatmap"])
