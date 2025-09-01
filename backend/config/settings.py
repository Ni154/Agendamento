from pydantic import BaseModel
import os

class Settings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./local.db")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-secret")
    JWT_EXPIRES_MIN: int = int(os.getenv("JWT_EXPIRES_MIN", "120"))
    ALLOWED_ORIGINS_RAW: str = os.getenv("ALLOWED_ORIGINS","*")
    ADMIN_TOKEN: str = os.getenv("ADMIN_TOKEN","admin-token")
    ENV: str = os.getenv("ENV","development")
    ALLOWED_ORIGIN_REGEX_FALLBACK: str = os.getenv(
        "ALLOWED_ORIGIN_REGEX",
        r"^https://([a-z0-9-]+\.)*(seusite\.com|netlify\.app)$|^http://(localhost|127\.0\.0\.1)(:\d+)?$"
    )

    @property
    def ALLOWED_ORIGINS(self) -> list[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS_RAW.split(",") if o.strip()]

settings = Settings()

