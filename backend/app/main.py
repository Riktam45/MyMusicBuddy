from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.users.model import User
from app.music.model import Song
from app.core.config import settings
from app.core.database import Base
from app.core.database import engine
from app.ai.models.loaders import load_models

from app.api.v1.api import api_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

# Load AI models when the application starts
load_models()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "project": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "Running",
    }