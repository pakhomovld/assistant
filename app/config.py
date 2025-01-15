from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env файла
load_dotenv()

class Settings:
    # Конфигурация для Yandex API
    IAM_TOKEN = os.getenv("IAM_TOKEN")
    FOLDER_ID = os.getenv("FOLDER_ID")
    OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")
    
    # URL базы данных
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # Секретный ключ для сессий
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    
    # Настройки для отладки
    DEBUG = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")
    
    # Настройки для базы данных (PostgreSQL)
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "assistant_db")
    DB_USER = os.getenv("DB_USER", "assistant_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "yourpassword")
    
    # Формирование URL базы данных, если DATABASE_URL отсутствует
    @property
    def database_url(self):
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
