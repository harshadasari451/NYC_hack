import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # Google AI
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_CLOUD_PROJECT: str = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    
    # App
    APP_NAME: str = os.getenv("APP_NAME", "MomAvatar")
    UPLOAD_DIR: Path = Path(os.getenv("UPLOAD_DIR", "./uploads"))
    CORS_ORIGINS: list[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    
    # Persona
    DEFAULT_RELATIONSHIP: str = os.getenv("DEFAULT_RELATIONSHIP", "daughter")
    DEFAULT_AVATAR_NAME: str = os.getenv("DEFAULT_AVATAR_NAME", "Mom")
    
    def __init__(self):
        # Ensure upload directory exists
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        (self.UPLOAD_DIR / "whatsapp").mkdir(exist_ok=True)
        (self.UPLOAD_DIR / "photos").mkdir(exist_ok=True)
        (self.UPLOAD_DIR / "audio_video").mkdir(exist_ok=True)


settings = Settings()
