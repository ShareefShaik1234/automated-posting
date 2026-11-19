import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.schemas import PlatformPostResult


class GitHubGistPlatform(BasePlatform):
    name = "GitHub Gist"
    API_URL = "https://api.github.com/gists"

    async def publish(self, message: str, client: httpx.AsyncClient) -> PlatformPostResult:
        if not settings.github_token:
            return self._failure_result("Missing GITHUB_TOKEN environment variable")

        headers = {
            "Authorization": f"Bearer {settings.github_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        payload = {
            "description": message[:80],
            "public": True,
            "files": {
                "announcement.md": {
                    "content": f"# Announcement\n\n{message}\n"
                }
            },
        }

        try:
            response = await client.post(self.API_URL, json=payload, headers=headers)
            if response.status_code == 201:
                data = response.json()
                return self._success_result(posted_url=data["html_url"], public_access=True)
            return self._failure_result(f"HTTP {response.status_code}: {response.text[:150]}")
        except httpx.RequestError as exc:
            return self._failure_result(f"Network error: {str(exc)}")
