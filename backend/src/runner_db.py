from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os

engine = create_engine(os.getenv('DATABASE_URL'))
Session = scoped_session(sessionmaker(bind=engine)) 