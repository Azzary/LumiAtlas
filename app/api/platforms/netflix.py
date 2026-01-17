from fastapi import APIRouter, Query
from datetime import date, timedelta
from typing import Literal

from app.tmdb.client import TMDBClient
from app.models.media_card import MediaCard
from app.tmdb.mappers import to_media_card
from app.core.settings import settings

router = APIRouter(prefix="/platform/netflix", tags=["netflix"])

NETFLIX_ID = 8


def base_params(page: int = 1):
    return {
        "language": settings.DEFAULT_LANGUAGE,
        "with_watch_providers": NETFLIX_ID,
        "watch_region": settings.DEFAULT_REGION,
        "page": page,
    }


async def discover(media_type: Literal["movie", "tv"], extra: dict):
    client = TMDBClient()
    data = await client.get(
        f"/discover/{media_type}",
        {**base_params(extra.get("page", 1)), **extra},
    )
    await client.aclose()
    return [
        to_media_card({**x, "media_type": media_type})
        for x in data.get("results", [])
    ]


@router.get("/top10", response_model=list[MediaCard])
async def netflix_top10():
    movies = await discover("movie", {"sort_by": "popularity.desc"})
    tv = await discover("tv", {"sort_by": "popularity.desc"})
    return (movies + tv)[:10]


@router.get("/new", response_model=list[MediaCard])
async def netflix_new():
    today = date.today()
    last_year = today - timedelta(days=365)

    movies = await discover(
        "movie",
        {
            "sort_by": "primary_release_date.desc",
            "primary_release_date.gte": last_year.isoformat(),
            "primary_release_date.lte": today.isoformat(),
        },
    )

    tv = await discover(
        "tv",
        {
            "sort_by": "first_air_date.desc",
            "first_air_date.gte": last_year.isoformat(),
            "first_air_date.lte": today.isoformat(),
        },
    )

    return movies + tv


@router.get("/popular", response_model=list[MediaCard])
async def netflix_popular(
    type: Literal["all", "movie", "tv"] = Query("all"),
):
    if type == "movie":
        return await discover("movie", {"sort_by": "popularity.desc"})

    if type == "tv":
        return await discover("tv", {"sort_by": "popularity.desc"})

    movies = await discover("movie", {"sort_by": "popularity.desc"})
    tv = await discover("tv", {"sort_by": "popularity.desc"})
    return movies + tv


@router.get("/catalog", response_model=list[MediaCard])
async def netflix_catalog(
    type: Literal["all", "movie", "tv"] = Query("all"),
    page: int = Query(1, ge=1),
):
    if type == "movie":
        return await discover("movie", {"sort_by": "popularity.desc", "page": page})

    if type == "tv":
        return await discover("tv", {"sort_by": "popularity.desc", "page": page})

    movies = await discover("movie", {"sort_by": "popularity.desc", "page": page})
    tv = await discover("tv", {"sort_by": "popularity.desc", "page": page})
    return movies + tv
