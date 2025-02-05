import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from models import Base
from database import DATABASE_URL

async def init_db():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())