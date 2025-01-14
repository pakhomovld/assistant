from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    IAM_TOKEN = os.getenv("IAM_TOKEN")
    FOLDER_ID = os.getenv("FOLDER_ID")
    OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

settings = Settings()

