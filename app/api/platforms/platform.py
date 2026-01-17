from fastapi import APIRouter
from app.tmdb.client import TMDBClient
from app.models.media_card import MediaCard
from app.core.settings import settings

router = APIRouter()

MAJOR_PLATFORMS = {
    "netflix",
    "amazon prime video",
    "disney plus",
    "apple tv plus",
    "canal+",
    "paramount plus",
    "hbo max",
    "hulu",
    "youtube premium",
}


IMAGE_BASE = "https://image.tmdb.org/t/p/w342"


@router.get("/platforms", response_model=list[MediaCard])
async def platforms():
    client = TMDBClient()

    movie = await client.get(
        "/watch/providers/movie",
        {"language": settings.DEFAULT_LANGUAGE},
    )
    tv = await client.get(
        "/watch/providers/tv",
        {"language": settings.DEFAULT_LANGUAGE},
    )

    seen: set[int] = set()
    cards: list[MediaCard] = []

    def ingest(items: list[dict]):
        for p in items:
            name = p["provider_name"].lower()

            if name not in MAJOR_PLATFORMS:
                continue

            pid = p["provider_id"]
            if pid in seen:
                continue

            seen.add(pid)

            cards.append(
                MediaCard(
                    id=pid,
                    media_type="platform",
                    title=p["provider_name"],
                    poster_url=(
                        f"{IMAGE_BASE}{p['logo_path']}"
                        if p.get("logo_path")
                        else None
                    ),
                )
            )

    ingest(movie.get("results", []))
    ingest(tv.get("results", []))

    cards.sort(key=lambda c: c.title.lower())
    return cards
