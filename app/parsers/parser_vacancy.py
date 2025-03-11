from typing import List, Generator
import requests
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent
from shared.Enums.vacancy_parms_validation import *

def build_vacancy_search_url(
    text: str,
    education: Vacancy_Education,
    part_time: Vacancy_PartTime,
    experience: Vacancy_Experience,
    schedule: Vacancy_Schedule,
    page: int
) -> str:
    base_url = "https://hh.ru/search/vacancy?hhtmFrom=main&hhtmFromLabel=vacancy_search_line&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&L_save_area=true&area=113"
    params = {
        "text": text,
        "part_time": part_time.value if part_time else "",
        "schedule":  schedule.value if schedule else "",
        "experience": experience.value if experience else "",
        "education": education.value if education else "",
        "page": page
    }
    return f"{base_url}{'&'.join(f'{k}={v}' for k, v in params.items() if v)}"

def parse_vacancy_links(html: str) -> List[str]:
    soup = BeautifulSoup(html, "lxml")
    links = []
    for item in soup.select(".vacancy-serp-content div:not([class])"):
        h2 = item.find("h2", {"data-qa": "bloko-header-2"})
        if h2 and (link := h2.find("a", href=True)):
            href = link["href"].split("?")[0]
            if "click" not in href:
                links.append(f"https://api.hh.ru{href}")
    return links

def get_vacancy_links(
    text: str,
    education: Vacancy_Education,
    part_time: Vacancy_PartTime,
    experience: Vacancy_Experience,
    schedule: Vacancy_Schedule,
    max_count: int = 1
) -> Generator[str, None, None]:
    user_agent = UserAgent()
    session = requests.Session()
    session.headers.update({'User-Agent': user_agent.random})

    current_page = 0
    pages_processed = 0
    
    while True:
        if max_count > 0 and pages_processed >= max_count:
            break
            
        url = build_vacancy_search_url(
            text, education, part_time, experience, schedule, current_page
        )
        
        try:
            response = session.get(url)
            response.raise_for_status()
            
            links = parse_vacancy_links(response.text)
            yield from links
            
            pages_processed += 1
            current_page += 1
            time.sleep(3)
            
        except requests.HTTPError as e:
            print(f"Ошибка при запросе страницы {current_page}: {str(e)}")
            break
        except Exception as e:
            print(f"Общая ошибка: {str(e)}")
            break

def get_vacancy_data(link: str):
    try:
        if session.query(Vacancy).filter_by(url=link).first():
            return

        response = requests.get(link, headers={"user-agent": "Parser/1.0"})
        if response.status_code != 200:
            return

        vacancy_data = response.json()
        
        new_vacancy = Vacancy(
            url=link,
            name=vacancy_data.get("name"),
            area=vacancy_data.get("area", {}).get("name"),
            salary_from=vacancy_data.get("salary", {}).get("from", 0),
            salary_to=vacancy_data.get("salary", {}).get("to", 0),
            experience=vacancy_data.get("experience", {}).get("name"),
            schedule=vacancy_data.get("schedule", {}).get("name"),
            employment=vacancy_data.get("employment", {}).get("name"),
            contacts=vacancy_data.get("contacts"),
            description=BeautifulSoup(vacancy_data.get("description", ""), "lxml").text,
            key_skills=[skill.get("name") for skill in vacancy_data.get("key_skills", [])],
            driver_license=[license.get("name") for license in vacancy_data.get("driver_license_types", [])],
            employer_name=vacancy_data.get("employer", {}).get("name"),
            languages=[lang.get("name") for lang in vacancy_data.get("languages", [])]
        )

        session.add(new_vacancy)
        session.commit()
        print("Вакансия сохранена")

    except Exception as e:
        print(f"Ошибка при обработке {link}: {str(e)}")
        return 1, link