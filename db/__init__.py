from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Base for all models
Base = declarative_base()

# Database URL
DATABASE_URL = "sqlite:///gym_manager.db"

# Engine & Session
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Import models so they are registered with Base, then create all tables.
    """
    import db.models  # ensures models are registered with Base
    Base.metadata.create_all(bind=engine)
