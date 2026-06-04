from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.config import settings

Base = declarative_base()

engine = create_async_engine(settings.DATABASE_URL, echo=True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False )