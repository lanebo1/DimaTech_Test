from fastapi import FastAPI
import routes
from database.database import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(routes.meta())
