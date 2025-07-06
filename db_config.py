# db_config.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL connection string
# Replace with your actual database credentials
DB_USER_PASSWORD = "cKj4adxL!MEJm9#CWeM"
DATABASE_URL = f"postgresql://society_app:{DB_USER_PASSWORD}@localhost:5432/society_db"
# DATABASE_URL = "postgresql://username:password@localhost:5432/society_db"


# Create SQLAlchemy engine
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