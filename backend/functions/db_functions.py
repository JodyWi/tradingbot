from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration
DATABASE_URL = 'sqlite:////home/ubuntu/job_hunter/database/local.db'

# Setting up the engine, session, and base
engine = create_engine(DATABASE_URL, echo=True)  # echo=True will log SQL queries, useful for debugging
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    password = Column(String, nullable=False)  # In real-world apps, store hashed passwords

# Function to create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Function to add a new user
def add_user(name, surname, email, phone, password):
    db = SessionLocal()
    user = User(name=name, surname=surname, email=email, phone=phone, password=password)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise e
    finally:
        db.close()

# Function to get a user by email
def get_user_by_email(email):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        return user
    finally:
        db.close()