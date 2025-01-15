import sys
import os

# Добавляем путь к модулю, если он не установлен
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from sqlalchemy import text
from app.models import User, Base, engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from bcrypt import hashpw, gensalt
import time


def hash_password(password: str) -> str:
    """Хэширует пароль перед сохранением."""
    return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")


def wait_for_db():
    """Ждет, пока база данных станет доступной."""
    while True:
        try:
            # Проверяем доступность базы данных с помощью соединения
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))  # Используем text() для запроса
            print("Database is ready!")
            break
        except OperationalError as e:
            print(f"Waiting for database... Error: {e}")
            time.sleep(2)


def initialize_users():
    """Инициализирует пользователей в базе данных."""
    session = Session(bind=engine)
    try:
        # Проверяем, существует ли пользователь с именем admin
        admin_user = session.query(User).filter_by(username="admin").first()
        if not admin_user:
            # Создаем нового пользователя с хэшированным паролем
            password_hash = hash_password("securepassword")  # Замените "securepassword" на ваш пароль
            new_user = User(username="admin", password_hash=password_hash)
            session.add(new_user)
            session.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists.")
    except Exception as e:
        print(f"Error initializing users: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    print("Waiting for database...")
    wait_for_db()
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Initializing default users...")
    initialize_users()
    print("Database initialization completed successfully!")
