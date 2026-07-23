from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
# ایجاد مدل پایه برای SQLAlchemy
Base = declarative_base()

# URL پایگاه داده SQLite

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver:5432/test.db"
# SQLALCHEMY_DATABASE_URL = "mysql://user:password@localhost/test.db"


# ایجاد موتور برای اتصال به پایگاه داده
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False})

# ساخت session ساز برای تعامل با پایگاه داده
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String())

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
