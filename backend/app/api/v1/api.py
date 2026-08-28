from fastapi import APIRouter

from app.api.v1.users import router as users_router
from app.api.v1.auth import router as auth_router
from app.api.v1.admin import router as admin_router
from app.api.v1.music import router as music_router
from app.api.v1.analysis import router as analysis_router
from app.api.v1.realtime import router as realtime_router
from app.api.v1.fretboard import router as fretboard_router


api_router = APIRouter(prefix="/api/v1")
api_router.include_router(admin_router)
api_router.include_router(users_router)
api_router.include_router(auth_router)
api_router.include_router(music_router)
api_router.include_router(analysis_router)
api_router.include_router(realtime_router)
api_router.include_router(fretboard_router)