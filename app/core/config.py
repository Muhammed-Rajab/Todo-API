from pathlib import Path
from pydantic import BaseSettings, AnyUrl

class Settings(BaseSettings):
    
    MONGODB_URL: AnyUrl = "mongodb://127.0.0.1:27017/"
    JWT_SECRET: str
    JWT_ALGORITHM: str
    STATICFILES_DIR: str = "static"
    STATICFILES_URI: str = "/static"
    BASE_PATH = Path(__file__).resolve().parent.parent
    PROFILEPICTURES_DIR: str = STATICFILES_DIR + "/images/profile_pictures/"
    ACCESS_TOKEN_EXPIRATION_TIME: float = 60 * 60
    class Config:
        
        # Path to .env file where secrets are stored
        env_file = str(Path(__file__).resolve().parent.parent / '.env')

settings = Settings()