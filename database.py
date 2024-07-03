from sqlalchemy import create_engine, Column, Integer, String, Text, Table, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import sessionmaker
from ParserHH.url import URL
Base = declarative_base()
engine = create_engine(URL)
class Vacancy(Base):
    __tablename__ = 'vacancies'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    name = Column(String)
    area = Column(String)
    salary_from = Column(Integer)
    salary_to = Column(Integer)
    experience = Column(String)
    schedule = Column(String)
    employment = Column(String)
    contacts = Column(Text)
    description = Column(Text)
    key_skills = Column(ARRAY(String))
    driver_license = Column(ARRAY(String))
    employer_name = Column(String)
    languages = Column(ARRAY(String))

class Resume(Base):
    __tablename__ = 'resumes'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    sex = Column(String)
    age = Column(Integer)
    job_search_status = Column(String)
    personal_address = Column(Text)
    position = Column(String)
    specialization = Column(String)
    busyness = Column(String, nullable=True)
    work_schedule = Column(String)
    experience = Column(Integer)
    skills = Column(ARRAY(String))
    about_me = Column(Text)
    education = Column(Text)
    language = Column(ARRAY(String))




Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
