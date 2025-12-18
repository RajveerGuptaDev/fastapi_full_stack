from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = (
    "postgresql+psycopg2://postgres:root@localhost:5432/got"
)

engine = create_engine(
    DATABASE_URL,
    echo=True
)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()