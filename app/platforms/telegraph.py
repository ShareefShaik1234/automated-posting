import json
import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformPostResult


class TelegraphPlatform(BasePlatform):
    name = "Telegraph"
    API_URL = "https://api.telegra.ph/createPage"

    async def publish(self, message: str, client: httpx.AsyncClient) -> PlatformPostResult:
        if not settings.telegraph_access_token:
            return self._failure_result("Missing TELEGRAPH_ACCESS_TOKEN environment variable")

        content_nodes = [{"tag": "p", "children": [message]}]
        payload = {
            "access_token": settings.telegraph_access_token,
            "title": message[:60],
            "content": json.dumps(content_nodes),
            "return_content": False,
        }

        try:
            response = await client.post(self.API_URL, data=payload)
            data = response.json()
            if response.status_code == 200 and data.get("ok"):
                return self._success_result(
                    posted_url=data["result"]["url"],
                    public_access=True,
                )
            return self._failure_result(data.get("error", f"HTTP {response.status_code}"))
        except httpx.RequestError as exc:
            return self._failure_result(f"Network error: {str(exc)}")
