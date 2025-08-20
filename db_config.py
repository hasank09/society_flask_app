# db_config.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL connection string
# Use environment variable for Render PostgreSQL or fallback to local
DATABASE_URL = os.environ.get(
    'R_EXT_DB_URL',  # Render provides this automatically
    'postgresql://society_app:cKj4adxL!MEJm9#CWeM@localhost:5432/society_db'  # Fallback for local development
)

# Handle potential SSL requirement for Render
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# Create SQLAlchemy engine
# Add SSL mode for production (Render requires SSL)
if 'localhost' not in DATABASE_URL:
    engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
else:
    engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()