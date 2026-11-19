from datetime import datetime, timezone
import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformPostResult


class DevToPlatform(BasePlatform):
    name = "Dev.to"
    API_URL = "https://dev.to/api/articles"

    async def publish(self, message: str, client: httpx.AsyncClient) -> PlatformPostResult:
        if not settings.devto_api_key:
            return self._failure_result("Missing DEVTO_API_KEY environment variable")

        headers = {
            "api-key": settings.devto_api_key,
            "Content-Type": "application/json",
            "Accept": "application/vnd.forem.api-v1+json",
        }
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        payload = {
            "article": {
                "title": f"Update ({timestamp}): {message[:55]}",
                "published": True,
                "body_markdown": message,
                "tags": ["news", "announcement"],
            }
        }

        try:
            response = await client.post(self.API_URL, json=payload, headers=headers)
            if response.status_code in (200, 201):
                data = response.json()
                return self._success_result(posted_url=data["url"], public_access=True)
            return self._failure_result(f"HTTP {response.status_code}: {response.text[:150]}")
        except httpx.RequestError as exc:
            return self._failure_result(f"Network error: {str(exc)}")
