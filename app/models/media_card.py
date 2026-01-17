from pydantic import BaseModel
from typing import Literal, Optional


class MediaCard(BaseModel):
    id: int
    media_type: Literal["movie", "tv", "platform", "genre"]

    title: str
    year: Optional[str] = None

    poster_url: Optional[str] = None
    backdrop_url: Optional[str] = None

    popularity: Optional[float] = None
    rating: Optional[float] = None
