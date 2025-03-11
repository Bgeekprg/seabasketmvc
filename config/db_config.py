# Importing libraries
from sqlalchemy import MetaData
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
import os
from sqlalchemy.ext.declarative import declarative_base

# Initialization
meta = MetaData()


# Creating engine
auth = f"{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
engine = create_engine(
    f"mysql+mysqlconnector://{auth}@{os.getenv('DATABASE_URL')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}",
    pool_recycle=3600,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base(metadata=meta)
