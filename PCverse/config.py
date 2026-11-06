import os


class Config:
    SECRET_KEY = os.environ.get("PCVERSE_SECRET_KEY") or os.urandom(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "PCVERSE_DATABASE_URI",
        "sqlite:///site.db"
    )
    CORS_ORIGINS = [
        origin.strip()
        for origin in os.environ.get(
            "PCVERSE_CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173"
        ).split(",")
        if origin.strip()
    ]
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = (
        os.environ.get("PCVERSE_COOKIE_SECURE", "false").lower() == "true"
    )