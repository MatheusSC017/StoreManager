import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Lu Style API"
    VERSION: str = "1.0.0"
    SENTRY_DSN: str = os.getenv("SENTRY_DSN")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    STATIC_DIR: str = "static/images"


settings = Settings()
