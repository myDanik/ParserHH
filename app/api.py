from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import session, Resume, Vacancy, Base, engine
from parsers.parser_resume import get_resume_links, get_resume_data
from parsers.parser_vacancy import get_vacancy_links, get_vacancy_data

app = FastAPI(title="ParserHH")

def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()

def clear_database():
    meta = Base.metadata
    for table in reversed(meta.sorted_tables):
        session.execute(table.delete())
    session.commit()

def process_entities(links_func, process_func, model, db: Session):
    new_links = list(links_func)
    
    existing_links = [item.url.strip() for item in db.query(model).all()]
    
    if sorted(new_links) != sorted(existing_links):
        clear_database()
        for link in new_links:
            process_func(link)
    
    return db.query(model).all()

@app.get("/resume")
def get_resumes(
    text: str,
    relocation: str,
    sex: str,
    job_search_status: str,
    employment: str,
    schedule: str,
    experience: str,
    education: str,
    count: int = 1,
    db: Session = Depends(get_db)
):
    links_gen = get_resume_links(
        text=text,
        relocation=relocation,
        sex=sex,
        job_search_status=job_search_status,
        employment=employment,
        schedule=schedule,
        experience=experience,
        education=education,
        max_count=count
    )
    
    resumes = process_entities(links_gen, get_resume_data, Resume, db)
    return {"data": [{"id": resume.id,
            "url": resume.url,
            "sex": resume.sex,
            "age": resume.age,
            "job_search_status": resume.job_search_status,
            "personal_address": resume.personal_address,
            "position": resume.position,
            "specialization": resume.specialization,
            "busyness": resume.busyness,
            "work_schedule": resume.work_schedule,
            "experience": resume.experience,
            "skills": [skill for skill in resume.skills],
            "about_me": resume.about_me,
            "education": resume.education,
            "languages": [language for language in resume.language]} for r in resumes]} 

@app.get("/vacancy")
def get_vacancies(
    text: str,
    education: str,
    part_time: str,
    experience: str,
    schedule: str,
    count: int = 1,
    db: Session = Depends(get_db)
):
    links_gen = get_vacancy_links(
        text=text,
        education=education,
        part_time=part_time,
        experience=experience,
        schedule=schedule,
        max_count=count
    )
    
    vacancies = process_entities(links_gen, get_vacancy_data, Vacancy, db)
    return {"data": [{"id": vacancy.id,
            "url": vacancy.url,
            "name": vacancy.name,
            "area": vacancy.area,
            "salary_from": vacancy.salary_from,
            "salary_to": vacancy.salary_to,
            "experience": vacancy.experience,
            "schedule": vacancy.schedule,
            "employment": vacancy.employment,
            "contacts": vacancy.contacts,
            "description": vacancy.description,
            "key_skills": vacancy.key_skills,
            "driver_license": vacancy.driver_license,
            "employer_name": vacancy.employer_name,
            "languages": vacancy.languages} for v in vacancies]}