from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.auth import authenticate_user
from app.core.security import create_access_token
from app.schemas.auth import Token,LoginRequest

router = APIRouter()

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def json_login(login: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, login.email, login.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
