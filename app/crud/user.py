from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.user import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: UserCreate):
    hashed_pw = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw,
        is_active=True,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
