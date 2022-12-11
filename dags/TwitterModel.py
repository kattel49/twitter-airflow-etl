from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
DB_DATABASE = os.getenv("DB_DATABASE")

Base = declarative_base()

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}")

Session = sessionmaker(bind=engine)
session = Session()

class Tweets(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    user = Column(String(15))
    text = Column(String)
    favorite_count = Column(Integer)
    retweet_count = Column(Integer)


if __name__ == "__main__":
    Base.metadata.create_all(engine)