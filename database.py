from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

DATABASE_URL = "postgresql://postgres:password123@localhost:5432/ums"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)
