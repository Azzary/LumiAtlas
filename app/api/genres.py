from fastapi import APIRouter
from app.tmdb.client import TMDBClient
from app.models.media_card import MediaCard
from app.core.settings import settings

router = APIRouter()

@router.get("/genres", response_model=list[MediaCard])
async def genres():
    client = TMDBClient()

    movie = await client.get(
        "/genre/movie/list",
        {"language": settings.DEFAULT_LANGUAGE},
    )
    tv = await client.get(
        "/genre/tv/list",
        {"language": settings.DEFAULT_LANGUAGE},
    )

    seen: set[int] = set()
    cards: list[MediaCard] = []

    def ingest(items: list[dict]):
        for g in items:
            name = g["name"]


            gid = g["id"]
            if gid in seen:
                continue

            seen.add(gid)

            cards.append(
                MediaCard(
                    id=gid,
                    media_type="genre",
                    title=name,
                )
            )

    ingest(movie.get("genres", []))
    ingest(tv.get("genres", []))

    cards.sort(key=lambda c: c.title.lower())
    return cards
