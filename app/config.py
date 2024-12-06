from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Image Search People API"
    
    # File Upload Settings
    DATASET_FOLDER: str = "dataset/persons"
    DATASET_LOST_FOLDER: str = "dataset/lost-persons"
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: set = {".jpg", ".jpeg", ".png"}
    
    # Elasticsearch Settings
    ELASTICSEARCH_HOST: str = os.getenv("ELASTICSEARCH_HOST", "localhost")
    ELASTICSEARCH_PORT: int = int(os.getenv("ELASTICSEARCH_PORT", "9200"))
    ELASTICSEARCH_INDEX: str = os.getenv("ELASTICSEARCH_INDEX", "people-image-facenet")
    ELASTICSEARCH_USERNAME: str = os.getenv("ELASTICSEARCH_USERNAME", "admin")
    ELASTICSEARCH_PASSWORD: str = os.getenv("ELASTICSEARCH_PASSWORD", "4dm1nus3r")
    ELASTICSEARCH_URL: str = f"http://{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}"
    ELASTICSEARCH_SEARCH_SIZE: int = 3
    ELASTICSEARCH_SEARCH_THRESHOLD: float = 0.89
    
    # CORS Settings
    CORS_ORIGINS: list = [
        "http://localhost:8100",
        "http://localhost:8000",
    ]
    
    # Cache Settings
    CACHE_TTL: int = 3600  # 1 hour
    
    # Logging Settings
    LOG_FILE: str = "app.log"
    LOG_MAX_BYTES: int = 1024 * 1024  # 1MB
    LOG_BACKUP_COUNT: int = 5
    
    class Config:
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()
