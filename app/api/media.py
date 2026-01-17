from fastapi import APIRouter, Path
from app.tmdb.client import TMDBClient
from app.models.media_details import MediaDetails, SeasonInfo, EpisodeInfo
from app.core.settings import settings

router = APIRouter()

IMAGE_POSTER = "https://image.tmdb.org/t/p/w342"
IMAGE_BACKDROP = "https://image.tmdb.org/t/p/w780"


@router.get("/media/{type}/{tmdb_id}", response_model=MediaDetails)
async def media_details(
    type: str = Path(..., pattern="^(movie|tv)$"),
    tmdb_id: int = Path(..., ge=1),
):
    client = TMDBClient()

    data = await client.get(
        f"/{type}/{tmdb_id}",
        {
            "language": settings.DEFAULT_LANGUAGE,
            "append_to_response": "videos",
        },
    )

    if not data.get("overview") or not (data.get("title") or data.get("name")):
        data_en = await client.get(
            f"/{type}/{tmdb_id}",
            {
                "language": "en-US",
                "append_to_response": "videos",
            },
        )
    else:
        data_en = None

    def pick(field: str):
        return data.get(field) or (data_en.get(field) if data_en else None)

    videos = (data.get("videos") or {}).get("results", [])
    if not videos and data_en:
        videos = (data_en.get("videos") or {}).get("results", [])

    trailer = next(
        (
            v for v in videos
            if v.get("site") == "YouTube" and v.get("type") == "Trailer"
        ),
        None,
    )

    out = MediaDetails(
        id=data["id"],
        mediaType=type,
        title=pick("title") or pick("name"),
        overview=pick("overview"),
        posterUrl=(
            f"{IMAGE_POSTER}{data['poster_path']}"
            if data.get("poster_path")
            else None
        ),
        backdropUrl=(
            f"{IMAGE_BACKDROP}{data['backdrop_path']}"
            if data.get("backdrop_path")
            else None
        ),
        year=(pick("release_date") or pick("first_air_date") or "")[:4] or None,
        runtime=data.get("runtime"),
        genres=[g["name"] for g in data.get("genres", [])],
        trailerYoutubeKey=trailer["key"] if trailer else None,
        seasons=None,
    )

    if type == "tv":
        seasons: list[SeasonInfo] = []

        for s in data.get("seasons", []):
            sn = s.get("season_number", 0)
            if sn <= 0:
                continue

            season_data = await client.get(
                f"/tv/{tmdb_id}/season/{sn}",
                {"language": settings.DEFAULT_LANGUAGE},
            )

            if not season_data.get("episodes"):
                season_data = await client.get(
                    f"/tv/{tmdb_id}/season/{sn}",
                    {"language": "en-US"},
                )

            episodes = [
                EpisodeInfo(
                    id=ep["id"],
                    episodeNumber=ep["episode_number"],
                    name=ep["name"],
                    overview=ep.get("overview"),
                )
                for ep in season_data.get("episodes", [])
            ]

            seasons.append(
                SeasonInfo(
                    seasonNumber=sn,
                    episodeCount=len(episodes),
                    episodes=episodes,
                )
            )

        out.seasons = seasons

    return out
