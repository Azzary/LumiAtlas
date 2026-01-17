from fastapi import APIRouter, Query
from app.tmdb.client import TMDBClient
from app.models.media_card import MediaCard
from app.tmdb.mappers import to_media_card

router = APIRouter()


@router.get("/trending", response_model=list[MediaCard])
async def trending(
    type: str = Query("all", pattern="^(all|movie|tv)$"),
    window: str = Query("week", pattern="^(day|week)$"),
    limit: int = Query(40, ge=1, le=100),
):
    client = TMDBClient()

    data = await client.get(f"/trending/{type}/{window}")

    results = data.get("results", [])

    cards: list[MediaCard] = []
    seen: set[tuple[int, str]] = set()

    for item in results:
        media_type = item.get("media_type")
        tmdb_id = item.get("id")

        if media_type not in ("movie", "tv"):
            continue

        key = (tmdb_id, media_type)
        if key in seen:
            continue

        seen.add(key)
        cards.append(to_media_card(item))

        if len(cards) >= limit:
            break

    return cards
