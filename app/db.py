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
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY NOT NULL,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT,
        createdAt DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
        updatedAt DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime'))
                )

                """
            )
            logging.info("Database connected successfully!")
            yield db
        except Exception as e:
            logging.error("Database connection error!")
            logging.error(e)

# you don't need the finally that was here before because db you are getting is local to the function 
# and will be closed when the function ends
