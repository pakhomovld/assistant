from dotenv import load_dotenv
import os
from app.ya_token_refresh import get_iam_token

# Load environment variables from the .env file
load_dotenv()

class Settings:
    # Path to the JSON key for the service account
    SA_KEY_PATH = os.getenv("YANDEX_SA_KEY_PATH", "./secrets/sa_key.json")

    # Configuration for Yandex API
    FOLDER_ID = os.getenv("FOLDER_ID")
    IAM_TOKEN = get_iam_token(SA_KEY_PATH)  # Get a fresh IAM token

    # Database URL
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Secret key for sessions
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

    # Debug settings
    DEBUG = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")

    # Database settings (PostgreSQL)
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "assistant_db")
    DB_USER = os.getenv("DB_USER", "assistant_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "yourpassword")

    # Generate the database URL if DATABASE_URL is not provided
    @property
    def database_url(self):
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
