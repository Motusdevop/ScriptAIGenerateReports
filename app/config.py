from pydantic_settings import BaseSettings, SettingsConfigDict
from app.logger_config import logger


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )

    GEMINI_API_KEY: str
    BASE_URL: str = "https://fanfan.softium-deti.ru:820"


settings = Settings()
logger.info("⚙️ Settings loaded successfully")
