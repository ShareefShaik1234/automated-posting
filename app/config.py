from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    github_token: str = ""
    telegraph_access_token: str = ""
    pastebin_api_key: str = ""
    devto_api_key: str = ""
    mastodon_instance_url: str = "https://mastodon.social"
    mastodon_access_token: str = ""
    request_timeout: float = 15.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
