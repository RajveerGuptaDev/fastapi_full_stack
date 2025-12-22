from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = (
    "postgresql+psycopg2://postgres.pkpawzbwzyxigczgcsvn:Vveer9098%40123@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require"
)

engine = create_engine(
    DATABASE_URL,
    echo=True
)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()