import httpx
from app.core.settings import settings
from app.core.errors import upstream_error

HEADERS = {
    "Authorization": f"Bearer {settings.TMDB_API_TOKEN}",
    "Accept": "application/json",
}

class TMDBClient:
    def __init__(self):
        self._client = httpx.AsyncClient(
            base_url=settings.TMDB_BASE_URL,
            headers=HEADERS,
            timeout=httpx.Timeout(15.0),
        )

    async def get(self, path: str, params: dict | None = None) -> dict:
        try:
            r = await self._client.get(path, params=params or {})
            r.raise_for_status()
            return r.json()
        except httpx.HTTPStatusError as e:
            try:
                detail = e.response.json().get("status_message")
            except Exception:
                detail = str(e)
            raise upstream_error(f"TMDB error: {detail}", status_code=e.response.status_code)
        except httpx.RequestError as e:
            raise upstream_error(f"TMDB request failed: {e}")

    async def aclose(self):
        await self._client.aclose()
