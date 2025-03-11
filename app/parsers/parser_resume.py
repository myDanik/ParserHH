from typing import List, Generator
import requests
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent
from shared.Enums.resume_parms_validation import *

def build_resume_search_url(
    text: str,
    relocation: Resume_Relocation,
    sex: Resume_Sex,
    job_search_status: Resume_JobSearchStatus,
    employment: Resume_Employment,
    schedule: Resume_Schedule,
    experience: Resume_Experience,
    education: Resume_Education,
    page: int
) -> str:
    base_url = "https://hh.ru/search/resume?isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&hhtmFrom=vacancy_search_list&hhtmFromLabel=resume_search_line&search_period=0&order_by=relevance&filter_exp_period=all_time"
    params = {
        "text": text,
        "relocation": relocation.value if relocation else "",
        "gender": sex.value if sex else "",
        "job_search_status": job_search_status.value if job_search_status else "",
        "employment": employment.value if employment else "",
        "schedule":  schedule.value if schedule else "",
        "experience": experience.value if experience else "",
        "education": education.value if education else "",
        "page": page
    }
    return f"{base_url}{'&'.join(f'{k}={v}' for k, v in params.items() if v)}"

def parse_resume_links(html: str) -> List[str]:
    soup = BeautifulSoup(html, "lxml")
    links = []
    for item in soup.select(".resume-serp-content div:not([class])"):
        if link := item.find("a", href=True):
            href = link["href"].split("?")[0]
            links.append(f"https://hh.ru{href}")
    return links

def get_resume_links(
    text: str,
    relocation: Resume_Relocation,
    sex: Resume_Sex,
    job_search_status: Resume_JobSearchStatus,
    employment: Resume_Employment,
    schedule: Resume_Schedule,
    experience: Resume_Experience,
    education: Resume_Education,
    max_count: int = 1
) -> Generator[str, None, None]:
    user_agent = UserAgent()
    
    def fetch_page(page: int):
        url = build_resume_search_url(
            text, relocation, sex, job_search_status,
            employment, schedule, experience, education, page
        )
        return requests.get(url, headers={"user-agent": user_agent.random})
    
    current_page = 0
    while True:
        response = fetch_page(current_page)
        if response.status_code != 200:
            break
            
        yield from parse_resume_links(response.text)
        current_page += 1
        time.sleep(1)
        
        if current_page >= max_count and max_count != 0:
            break
    
def get_resume_data(link):
    try:
        if session.query(Resume).filter_by(url=link).first():
            return

        user_agent = UserAgent().random
        response = requests.get(link, headers={"user-agent": user_agent})
        if response.status_code != 200:
            return

        soup = BeautifulSoup(response.content, "lxml")
        
        resume_block = find_resume_block(soup)
        
        resume_data = {
            'url': link,
            'sex': get_sex(resume_block),
            'age': get_age(resume_block),
            'job_search_status': get_job_status(resume_block),
            'personal_address': get_address(resume_block),
            'position': get_position(resume_block),
            'specialization': get_specialization(resume_block),
            'busyness': get_busyness(resume_block),
            'work_schedule': get_work_schedule(resume_block),
            'experience': get_experience(resume_block),
            'skills': get_skills(resume_block),
            'about_me': get_about_me(resume_block),
            'education': get_education(resume_block),
            'language': get_languages(resume_block)
        }

        session.add(resume_data)
        session.commit()
        print("Резюме сохранено")

    except Exception as e:
        print(f"Ошибка при обработке {link}: {str(e)}")
        return 1, link

def find_resume_block(soup):
    blocks = soup.find_all("div", class_="bloko-columns-row")
    if len(blocks) >= 2:
        return blocks[1]
    return soup.find("div", class_="bloko-columns-wrapper")

def get_sex(block):
    elem = block.find("span", {"data-qa": "resume-personal-gender"})
    return elem.text if elem else None

def get_age(block):
    elem = block.find("span", {"data-qa": "resume-personal-age"})
    return int(elem.text[:2]) if elem else 0

def get_job_status(block):
    elem = block.find("div", class_="resume-job-search-status")
    return elem.text if elem else None

def get_address(block):
    elem = block.find("span", {"data-qa": "resume-personal-address"})
    return elem.text if elem else None

def get_position(block):
    elem = block.find("div", class_="resume-block-position")
    return elem.text if elem else None

def get_specialization(block):
    elem = block.find("li", class_="resume-block__specialization")
    return elem.text if elem else None

def get_busyness(block):
    paragraphs = block.find("div", class_="resume-block-container").find_all("p")
    return paragraphs[0].text if len(paragraphs) >= 1 else None

def get_work_schedule(block):
    paragraphs = block.find("div", class_="resume-block-container").find_all("p")
    return paragraphs[1].text if len(paragraphs) >= 2 else None

def get_experience(block):
    exp_block = block.find("span", class_="resume-block__title-text_sub")
    if not exp_block:
        return 0
    
    spans = exp_block.find_all("span")
    if len(spans) == 2:
        years = int(spans[0].text[:2])
        months = int(spans[1].text[:2])
        return years * 12 + months
    elif len(spans) == 1:
        return int(spans[0].text[:2])
    return 0

def get_skills(block):
    skills = block.find_all("div", class_="bloko-tag_inline")
    return [skill.text for skill in skills] if skills else []

def get_about_me(block):
    elem = block.find("div", {"data-qa": "resume-block-skills-content"})
    return elem.text if elem else None

def get_education(block):
    elem = block.find("div", {"data-qa": "resume-block-education"})
    return elem.text if elem else None

def get_languages(block):
    langs = block.find_all("div", class_="bloko-tag_inline")
    return [lang.text for lang in langs] if langs else []