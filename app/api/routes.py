from fastapi import APIRouter
from app.api.platforms.platform import router as platforms_router
from app.api.genres import router as genres_router
from app.api.trending import router as trending_router
from app.api.media import router as media_router
from app.api.catalog import router as catalog_router
from app.api.platforms.netflix import router as netflix_router
from app.api.search import router as search_router

router = APIRouter()

router.include_router(platforms_router, tags=["platforms"])
router.include_router(genres_router, tags=["genres"])
router.include_router(trending_router, tags=["trending"])
router.include_router(media_router, tags=["media"])
router.include_router(catalog_router, tags=["catalog"])
router.include_router(netflix_router, tags=["netflix"])
router.include_router(search_router, tags=["search"])
