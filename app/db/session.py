from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create async SQLAlchemy engine
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)

# Create async session maker
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency for routes
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
