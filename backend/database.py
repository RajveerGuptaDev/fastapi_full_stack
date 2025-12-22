from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = (
    "postgresql://postgres:Rrajveer576%40@db.pkpawzbwzyxigczgcsvn.supabase.co:5432/postgres"
)

engine = create_engine(
    DATABASE_URL,
    echo=True
)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()