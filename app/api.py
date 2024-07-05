from fastapi import FastAPI
from main import get_links, get_resume, get_links_vacancy, get_vacancy
from database import Resume, Vacancy, session, Base
from shared.Enums.resume_parms_validation import *
from shared.Enums.vacancy_parms_validation import *
app = FastAPI(title="ParserHH")
@app.get("/resume")
def resume_get(text: str, relocation: Resume_Relocation, sex: Resume_Sex, job_search_status: Resume_JobSearchStatus, employment: Resume_Employment, schedule: Resume_Schedule, experience: Resume_Experience, education: Resume_Education, count: int = 1):
    print("API")
    links = list(get_links(text,relocation,sex,job_search_status,employment,schedule,experience, education, count))
    print(f"Fetched links: {links}")
    existing_links = [resume.url.strip() for resume in session.query(Resume).all()]
    print(f"Existing links in DB: {existing_links}")

    if sorted(links) != sorted(existing_links):
        clear_database()
        print("Drop DB")
        for page in links:
            get_resume(page)

    resumes = session.query(Resume).all()

    result_list = []

    for resume in resumes:
        resume_dict = {
            "id": resume.id,
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
            "languages": [language for language in resume.language]
        }
        result_list.append(resume_dict)

    return {"status": "success",
            "data": result_list,
            "details": None
            }
@app.get("/vacancy")
def vacancy_get(text: str, education: Vacancy_Education, part_time: Vacancy_PartTime, experience: Vacancy_Experience, schedule: Vacancy_Schedule, count: int = 1):
    print(text)
    links = list(get_links_vacancy(text=text, education=education, part_time=part_time, experience=experience, schedule=schedule, count=count))
    print(f"Fetched links: {links}")
    existing_links = [vacancy.url.strip() for vacancy in session.query(Vacancy).all()]
    print(f"Existing links in DB: {existing_links}")


    if sorted(links)!=sorted(existing_links):
        clear_database()
        print("Drop DB")
        for page in links:
            get_vacancy(page)


    vacancies = session.query(Vacancy).all()

    result_list = []

    for vacancy in vacancies:
        vacancy_dict = {
            "id": vacancy.id,
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
            "languages": vacancy.languages
        }
        result_list.append(vacancy_dict)
    return {"status": "success",
     "data": result_list,
     "details": None
     }
def clear_database():

    meta = Base.metadata
    for table in reversed(meta.sorted_tables):
        session.execute(table.delete())
    session.commit()