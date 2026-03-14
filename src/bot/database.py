from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .config import settings
from .models import Base

engine = create_async_engine(url=settings.DATABASE_URL)
sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)


async def get_db_session():
    async with sessionmaker() as session:
        yield session


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def flush_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
