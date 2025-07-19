from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit= False, bind=engine)

Base = declarative_base()

def get_db():
  try:
    db = SessionLocal()
    yield db
  except Exception as e:
    print(f"DATABASE Session Error: {e}")
    raise e
  finally:
    db.close()
