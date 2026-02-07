from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

async_database_url = "postgresql+asyncpg://iot_admin:1234@localhost/iot_dashboard"
async_engine = create_async_engine(async_database_url)
async_session_local = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)