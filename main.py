from fastapi import FastAPI
import routes
from database.database import Base, engine, init_db

app = FastAPI()

app.include_router(routes.meta())

init_db()