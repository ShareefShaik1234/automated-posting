import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformPostResult


class MastodonPlatform(BasePlatform):
    name = "Mastodon"

    async def publish(self, message: str, client: httpx.AsyncClient) -> PlatformPostResult:
        if not settings.mastodon_access_token:
            return self._failure_result("Missing MASTODON_ACCESS_TOKEN environment variable")

        base_url = settings.mastodon_instance_url.rstrip("/")
        api_url = f"{base_url}/api/v1/statuses"
        headers = {
            "Authorization": f"Bearer {settings.mastodon_access_token}",
        }
        payload = {
            "status": message,
            "visibility": "public",
        }

        try:
            response = await client.post(api_url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return self._success_result(posted_url=data["url"], public_access=True)
            return self._failure_result(f"HTTP {response.status_code}: {response.text[:150]}")
        except httpx.RequestError as exc:
            return self._failure_result(f"Network error: {str(exc)}")
