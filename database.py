from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Boolean, ARRAY
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
Base = declarative_base()
engine = create_engine(url)
# Создание сессии для работы с базой данных
Session = sessionmaker(engine)
session = Session()