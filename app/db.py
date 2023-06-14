import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./d_b.db"

# Create the engine and database connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the Base Class for declarative models
Base = declarative_base()
Base.metadata.create_all(bind=engine)

#Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        logging.info("Database connected successfully!")
        yield db
    finally:
        db.close()
        logging.info("Database disconnected!")
