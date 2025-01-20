"""
Database initialization script.

This script initializes the database, creates default tables,
and adds an admin user if one does not exist.
"""

import sys
import os
import time
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from app.models import User, Base, engine
from bcrypt import hashpw, gensalt

# Add the parent directory to the system path for module resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))


def hash_password(password: str) -> str:
    """
    Hashes a password for secure storage.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        str: The hashed password.
    """
    return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")


def wait_for_db():
    """
    Waits until the database is ready to accept connections.

    Continuously attempts to connect to the database until successful.
    """
    while True:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database is ready!")
            break
        except OperationalError as e:
            print(f"Waiting for database... Error: {e}")
            time.sleep(2)


def initialize_users():
    """
    Initializes default users in the database.

    Creates an admin user with a default password if one does not already exist.
    """
    session = Session(bind=engine)
    try:
        admin_user = session.query(User).filter_by(username="admin").first()
        if not admin_user:
            password_hash = hash_password("securepassword")  # Replace with a secure password
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
