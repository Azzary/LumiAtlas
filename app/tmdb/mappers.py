from app.models.media_card import MediaCard
from app.models.media_details import MediaDetails


def to_media_card(tmdb: dict) -> MediaCard:
    return MediaCard(
        id=tmdb["id"],
        media_type=tmdb["media_type"],
        title=tmdb.get("title") or tmdb.get("name"),
        year=(tmdb.get("release_date") or tmdb.get("first_air_date") or "")[:4] or None,
        poster_url=(
            f"https://image.tmdb.org/t/p/w342{tmdb['poster_path']}"
            if tmdb.get("poster_path") else None
        ),
        backdrop_url=(
            f"https://image.tmdb.org/t/p/w780{tmdb['backdrop_path']}"
            if tmdb.get("backdrop_path") else None
        ),
        popularity=tmdb.get("popularity"),
        rating=tmdb.get("vote_average"),
    )
