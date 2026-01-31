from sqlalchemy.ext.asyncio import (AsyncSession, 
                                    AsyncEngine, 
                                    create_async_engine, 
                                    async_sessionmaker)
from core.configs import settings

engine: AsyncEngine = create_async_engine(settings.DB_URL)

Session = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)
