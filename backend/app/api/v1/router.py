from fastapi import APIRouter

from app.api.v1.endpoints import auth, entry, health, stats, tag, user

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(entry.router, prefix="/entries", tags=["entries"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(tag.router, prefix="/tags", tags=["tags"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])
