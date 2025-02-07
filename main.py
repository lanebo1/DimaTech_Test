from fastapi import FastAPI
import routes
from database.database import Base, engine

app = FastAPI()

app.include_router(routes.meta())

async def init_db():
    print("!!!Creating tables")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("!!!Tables created")

if __name__ == "__main__":
    init_db()