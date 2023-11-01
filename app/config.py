from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    VONAGE_API_KEY: str = "test"
    VONAGE_API_SECRET: str = "test"
    VONAGE_API_ROOT_URL: str = "https://api.nexmo.com/v2"
    VONAGE_API_BRAND_NAME: str = "Test"
    REDIS_CLIENT_HOST: str = "localhost"
    REDIS_CLIENT_PORT: int = 6379

    model_config = SettingsConfigDict(env_file="app/.env")
