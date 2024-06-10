from fastapi import FastAPI
from .database import engine
from .models import Base
from .views import router as views_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(views_router)