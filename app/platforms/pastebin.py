import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformPostResult


class PastebinPlatform(BasePlatform):
    name = "Pastebin"
    API_URL = "https://pastebin.com/api/api_post.php"

    async def publish(self, message: str, client: httpx.AsyncClient) -> PlatformPostResult:
        if not settings.pastebin_api_key:
            return self._failure_result("Missing PASTEBIN_API_KEY environment variable")

        payload = {
            "api_dev_key": settings.pastebin_api_key,
            "api_option": "paste",
            "api_paste_code": message,
            "api_paste_name": message[:50],
            "api_paste_private": "0",
            "api_paste_expire_date": "1M",
        }

        try:
            response = await client.post(self.API_URL, data=payload)
            body = response.text.strip()
            if response.status_code == 200 and body.startswith("https://pastebin.com/"):
                return self._success_result(posted_url=body, public_access=True)
            return self._failure_result(body or f"HTTP {response.status_code}")
        except httpx.RequestError as exc:
            return self._failure_result(f"Network error: {str(exc)}")
