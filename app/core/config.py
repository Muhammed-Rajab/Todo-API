from pathlib import Path
from pydantic import BaseSettings, AnyUrl

class Settings(BaseSettings):
    
    # Database
    MONGODB_URL: AnyUrl = "mongodb://127.0.0.1:27017/"

    # Authentication
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRATION_TIME: float = 60 * 60

    # Directories
    STATICFILES_DIR: str = "static"
    STATICFILES_URI: str = "/static"
    BASE_PATH = Path(__file__).resolve().parent.parent
    PROFILEPICTURES_DIR: str = STATICFILES_DIR + "/images/profile_pictures"
    PROFILE_PICTURE_FILENAME_LENGTH: int = 12
    PROFILE_PICTURE_FILESIZE: int = 4 * 1024 * 1024
    class Config:
        
        # Path to .env file where secrets are stored
        env_file = str(Path(__file__).resolve().parent.parent / '.env')

settings = Settings()