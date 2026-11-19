import asyncio
from typing import List
import httpx
from app.config import settings
from app.platforms.base import BasePlatform
from app.platforms.devto import DevToPlatform
from app.platforms.github_gist import GitHubGistPlatform
from app.platforms.mastodon import MastodonPlatform
from app.platforms.pastebin import PastebinPlatform
from app.platforms.telegraph import TelegraphPlatform
from app.schemas import PlatformPostResult, PostingResponse


class PostingService:
    def __init__(self, platforms: List[BasePlatform] | None = None) -> None:
        self.platforms: List[BasePlatform] = platforms or [
            GitHubGistPlatform(),
            TelegraphPlatform(),
            PastebinPlatform(),
            DevToPlatform(),
            MastodonPlatform(),
        ]

    async def _safe_publish(
        self, platform: BasePlatform, message: str, client: httpx.AsyncClient
    ) -> PlatformPostResult:
        try:
            return await platform.publish(message, client)
        except Exception as exc:
            return PlatformPostResult(
                platform=platform.name,
                status="failed",
                posted_url=None,
                public_access=False,
                date=None,
                time=None,
                error=f"Unexpected error: {str(exc)}",
            )

    async def publish_all(self, message: str) -> PostingResponse:
        async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
            tasks = [
                self._safe_publish(platform, message, client)
                for platform in self.platforms
            ]
            results = await asyncio.gather(*tasks)

        any_succeeded = any(item.status == "success" for item in results)
        return PostingResponse(success=any_succeeded, results=list(results))
