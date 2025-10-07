from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
# load_dotenv(dotenv_path="./.env")

# Get DB URL from .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
# print("👉 Using database URL:", SQLALCHEMY_DATABASE_URL)


if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL is missing. Please set it in your .env file.")

# Engine creation
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    # Only SQLite needs check_same_thread
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
