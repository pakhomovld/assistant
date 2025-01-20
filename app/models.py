from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

"""
Database models and setup for the application.
Defines the schema for tables and initializes the database engine.
"""

Base = declarative_base()
engine = create_engine(settings.get_database_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class QueryHistory(Base):
    """
    Model representing a history of user queries and responses.

    Attributes:
        id (int): Primary key for the record.
        username (str): Username of the user who made the query.
        question (str): The user's query.
        response (str): The response provided.
    """
    __tablename__ = "query_history"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    question = Column(Text, nullable=False)
    response = Column(Text, nullable=False)

class User(Base):
    """
    Model representing a user in the system.

    Attributes:
        id (int): Primary key for the user.
        username (str): Unique username for the user.
        password_hash (str): Hashed password for authentication.
        is_active (bool): Indicates if the user account is active.
        is_admin (bool): Indicates if the user has administrative privileges.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)


class UploadedDocument(Base):
    """
    Model representing uploaded documents.

    Attributes:
        id (int): Primary key for the document.
        username (str): Username of the uploader.
        file_name (str): Name of the uploaded file.
        content (str): Content of the uploaded file.
    """
    __tablename__ = "uploaded_documents"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    content = Column(Text, nullable=False)

# Ensure all tables are created
Base.metadata.create_all(bind=engine)
