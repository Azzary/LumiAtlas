from fastapi import APIRouter, Query
from typing import Literal, Optional
from datetime import date, timedelta

from app.tmdb.client import TMDBClient
from app.models.media_card import MediaCard
from app.core.settings import settings
from app.tmdb.mappers import to_media_card

router = APIRouter()

@router.get("/catalog", response_model=list[MediaCard])
async def catalog(
    type: Literal["all", "movie", "tv"] = Query("all"),
    platform: Optional[int] = Query(None, ge=1),
    genre_id: Optional[int] = Query(None, ge=1),
    year: Optional[int] = Query(None, ge=1900, le=2100),
    page: int = Query(1, ge=1, le=500),
):
    client = TMDBClient()

    async def discover(media_type: Literal["movie", "tv"]) -> list[MediaCard]:
        params: dict = {
            "language": settings.DEFAULT_LANGUAGE,
            "page": page,
            "sort_by": "popularity.desc",
        }

        if platform:
            params["with_watch_providers"] = str(platform)
            params["watch_region"] = settings.DEFAULT_REGION

        if genre_id:
            params["with_genres"] = str(genre_id)

        if year:
            if media_type == "movie":
                params["primary_release_year"] = str(year)
            else:
                params["first_air_date_year"] = str(year)

        today = date.today()
        if media_type == "movie":
            params["primary_release_date.gte"] = str(today - timedelta(days=365))
            params["primary_release_date.lte"] = str(today)
        else:
            params["first_air_date.gte"] = str(today - timedelta(days=365))
            params["first_air_date.lte"] = str(today)

        data = await client.get(f"/discover/{media_type}", params)

        return [
            to_media_card({**x, "media_type": media_type})
            for x in data.get("results", [])
        ]

    try:
        if type == "all":
            movies = await discover("movie")
            tv = await discover("tv")

            return movies + tv

        return await discover(type)

    finally:
        await client.aclose()
