from fastapi import FastAPI
from main import get_links, get_resume, get_links_vacancy, get_vacancy
from database import Resume, Vacancy, session, Base, engine
from Enums.resume_parms_validation import *
from Enums.vacancy_parms_validation import *
app = FastAPI(title="ParserHH")
@app.get("/resume")
def resume_get(text: str, relocation: Relocation, sex: Sex, job_search_status: JobSearchStatus, employment: Employment, schedule: Schedule, experience: Experience, education: Education):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    for page in get_links(text,relocation,sex,job_search_status,employment,schedule,experience,education):
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
            "skills": [skill.skill for skill in resume.skills],
            "about_me": resume.about_me,
            "education": resume.education,
            "languages": [language.language for language in resume.languages]
        }
        result_list.append(resume_dict)

    return {"status": "success",
            "data": result_list,
            "details": None
            }
@app.get("/vacancy")
def vacancy_get(text: str, education: Education, part_time: PartTime, experience: Experience, schedule: Schedule):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    for page in get_links_vacancy(text, education, part_time, experience, schedule):
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
