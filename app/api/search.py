from fastapi import APIRouter, Query
from typing import List
from app.tmdb.client import TMDBClient
from app.models.media_card import MediaCard
from app.tmdb.mappers import to_media_card
from app.core.settings import settings

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=List[MediaCard])
async def search(
    q: str = Query(..., min_length=2),
    page: int = Query(1, ge=1, le=500),
):
    client = TMDBClient()

    async def fetch(language: str):
        return await client.get(
            "/search/multi",
            {
                "query": q,
                "language": language,
                "page": page,
                "include_adult": False,
            },
        )

    try:
        data = await fetch(settings.DEFAULT_LANGUAGE)

        if not data.get("results"):
            data = await fetch("en-US")

        cards: list[MediaCard] = []

        for item in data.get("results", []):
            media_type = item.get("media_type")
            if media_type not in ("movie", "tv"):
                continue

            cards.append(
                to_media_card(
                    {
                        **item,
                        "media_type": media_type,
                    }
                )
            )

        return cards

    finally:
        await client.aclose()
