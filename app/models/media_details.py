from pydantic import BaseModel
from typing import Literal, Optional


class EpisodeInfo(BaseModel):
    id: int
    episodeNumber: int
    name: str
    overview: Optional[str] = None


class SeasonInfo(BaseModel):
    seasonNumber: int
    episodeCount: int
    episodes: list[EpisodeInfo]


class MediaDetails(BaseModel):
    id: int
    mediaType: Literal["movie", "tv"]

    title: str
    overview: Optional[str] = None

    posterUrl: Optional[str] = None
    backdropUrl: Optional[str] = None

    year: Optional[str] = None
    runtime: Optional[int] = None

    genres: list[str]

    trailerYoutubeKey: Optional[str] = None

    seasons: Optional[list[SeasonInfo]] = None
