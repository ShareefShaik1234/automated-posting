import re
from typing import List, Optional
from urllib.parse import urlparse
from pydantic import BaseModel, Field, field_validator


URL_REGEX = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)


class PostingRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        description="Short promotional message (max 200 chars) containing exactly one valid CTA URL.",
        examples=[
            "Check out our latest business platform and grow your online visibility. https://example.com"
        ],
    )

    @field_validator("message")
    @classmethod
    def validate_message_and_cta(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Message cannot be empty or whitespace only.")

        if len(cleaned) > 200:
            raise ValueError(
                f"Message must not exceed 200 characters (received {len(cleaned)} characters)."
            )

        urls = URL_REGEX.findall(cleaned)
        if len(urls) == 0:
            raise ValueError("Message must include exactly one CTA link (none found).")
        if len(urls) > 1:
            raise ValueError(
                f"Message must include exactly one CTA link (found {len(urls)} links)."
            )

        cta_url = urls[0]
        parsed = urlparse(cta_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc or "." not in parsed.netloc:
            raise ValueError(f"Invalid CTA URL provided: '{cta_url}'.")

        return cleaned


class PlatformPostResult(BaseModel):
    platform: str
    status: str  # "success" or "failed"
    posted_url: Optional[str] = None
    public_access: bool = False
    date: Optional[str] = None
    time: Optional[str] = None
    error: Optional[str] = None


class PostingResponse(BaseModel):
    success: bool
    results: List[PlatformPostResult]
