from fastapi.testclient import TestClient
import httpx
from app.main import app
from app.platforms.base import BasePlatform
from app.schemas import PlatformPostResult
from app.services.posting_service import PostingService

client = TestClient(app)


class MockSuccessPlatform(BasePlatform):
    name = "MockPlatformA"

    async def publish(self, message: str, http_client: httpx.AsyncClient) -> PlatformPostResult:
        return self._success_result("https://mockplatform.example.com/post/1")


class MockFailPlatform(BasePlatform):
    name = "MockPlatformB"

    async def publish(self, message: str, http_client: httpx.AsyncClient) -> PlatformPostResult:
        return self._failure_result("Authentication failed")


def test_validation_rejects_over_200_chars():
    long_msg = ("A" * 185) + " https://example.com"
    response = client.post("/posting", json={"message": long_msg})
    assert response.status_code == 422
    assert response.json()["success"] is False


def test_validation_rejects_missing_url():
    response = client.post("/posting", json={"message": "Hello world without any link!"})
    assert response.status_code == 422


def test_validation_rejects_multiple_urls():
    response = client.post(
        "/posting",
        json={"message": "Visit https://example.com and https://another.org today!"},
    )
    assert response.status_code == 422


def test_validation_rejects_malformed_url():
    response = client.post(
        "/posting",
        json={"message": "Broken link http://invalidurl without tld"},
    )
    assert response.status_code == 422


def test_independent_platform_execution(monkeypatch):
    mock_service = PostingService(platforms=[MockSuccessPlatform(), MockFailPlatform()])
    monkeypatch.setattr("app.main.posting_service", mock_service)

    response = client.post(
        "/posting",
        json={"message": "Check out our new product launch! https://example.com"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert len(body["results"]) == 2
    assert body["results"][0]["status"] == "success"
    assert body["results"][0]["posted_url"] == "https://mockplatform.example.com/post/1"
    assert body["results"][1]["status"] == "failed"
    assert body["results"][1]["error"] == "Authentication failed"
