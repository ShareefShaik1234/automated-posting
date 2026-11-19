from abc import ABC, abstractmethod
from datetime import datetime, timezone
import httpx
from app.schemas import PlatformPostResult


class BasePlatform(ABC):
    name: str = "Unknown Platform"

    @abstractmethod
    async def publish(self, message: str, client: httpx.AsyncClient) -> PlatformPostResult:
        """Publish the message to the third-party platform and return standardized result."""
        raise NotImplementedError

    def _success_result(self, posted_url: str, public_access: bool = True) -> PlatformPostResult:
        now = datetime.now(timezone.utc)
        return PlatformPostResult(
            platform=self.name,
            status="success",
            posted_url=posted_url,
            public_access=public_access,
            date=now.strftime("%Y-%m-%d"),
            time=now.strftime("%H:%M:%S"),
            error=None,
        )

    def _failure_result(self, error_message: str) -> PlatformPostResult:
        return PlatformPostResult(
            platform=self.name,
            status="failed",
            posted_url=None,
            public_access=False,
            date=None,
            time=None,
            error=error_message,
        )
