import requests
from bs4 import BeautifulSoup
import time
import fake_useragent
import json
import os


def get_links(text):
    useragent = fake_useragent.UserAgent()


    def get_total_pages():
        data = requests.get(
            url=f"https://hh.ru/search/resume?text={text}&area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&page=0",
            headers={"user-agent": useragent.random}
        )
        if data.status_code != 200:
            return 0
        soup = BeautifulSoup(data.content, "lxml")
        try:
            pages = int(
                soup.find(attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find("span").text)
            return pages
        except Exception as e:
            print(f"Error finding total pages: {e}")
            return 1

    total_pages = get_total_pages()

    for page in range(total_pages):
        data = requests.get(
            url=f"https://hh.ru/search/resume?text={text}&area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&page={page}",
            headers={"user-agent": useragent.random}
        )
        if data.status_code != 200:
            continue
        soup = BeautifulSoup(data.content, features="lxml")
        for i in soup.find(attrs={"class": "resume-serp-content"}).find_all("div", attrs={"class": None}):
            h3_tag = i.find("h3", attrs={"class": "bloko-header-section-3"})
            if h3_tag is not None:
                link = h3_tag.find("a")
                if link is not None:
                    yield f"https://hh.ru{link.attrs['href'].split('?')[0]}"

        time.sleep(1)


def get_resume(link):
    useragent = fake_useragent.UserAgent()
    data = requests.get(url=link, headers={"user-agent": useragent.random})
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")

    try:
        if len(soup.find_all("div", attrs={"class":"bloko-columns-row"}))>=2:
            resume = soup.find_all("div", attrs={"class":"bloko-columns-row"})[1]
        else:
            resume = soup.find("div", attrs={"class":"bloko-columns-wrapper"})
        if resume.find("span", attrs={"data-qa":"resume-personal-gender"}):
            sex = resume.find("span", attrs={"data-qa":"resume-personal-gender"}).text
        else:
            sex = None
        if resume.find("span", attrs={"data-qa":"resume-personal-age"}):
            age = int(resume.find("span", attrs={"data-qa":"resume-personal-age"}).text[:2])
        else:
            age = 0
        if resume.find("div", attrs={"class": "resume-job-search-status"}):
            job_search_status = resume.find("div", attrs={"class": "resume-job-search-status"}).text
        else:
            job_search_status = None
        if resume.find("div", attrs={"class":"bloko-translate-guard"}).find("span",attrs={"data-qa": "resume-personal-address"}):
            personal_adress = resume.find("div", attrs={"class":"bloko-translate-guard"}).find("span",attrs={"data-qa": "resume-personal-address"}).text
        else:
            personal_adress = None
        if resume.find("div", attrs={"class":"resume-block-position"}):
            position = resume.find("div", attrs={"class":"resume-block-position"}).text
        else:
            position = None
        if resume.find("li", attrs={"class":"resume-block__specialization"}):
            specialization = resume.find("li", attrs={"class":"resume-block__specialization"}).text
        else:
            specialization = None
        if resume.find("div", attrs={"class":"resume-block-container"}).find("p") and len(resume.find("div", attrs={"class":"resume-block-container"}).find_all("p"))==1:
            busyness = resume.find("div", attrs={"class":"resume-block-container"}).find_all("p")[0].text
        else:
            busyness = None

        if resume.find("div", attrs={"class":"resume-block-container"}).find("p") and len(resume.find("div", attrs={"class":"resume-block-container"}).find_all("p"))==2:
            work_schedule = resume.find("div", attrs={"class":"resume-block-container"}).find_all("p")[1].text
        else:
            work_schedule = None
        if resume.find("span", attrs={"class":"resume-block__title-text resume-block__title-text_sub"}).find("span") and len(resume.find("span", attrs={"class":"resume-block__title-text resume-block__title-text_sub"}).find_all("span")) == 2:
            experience = int(resume.find("span", attrs={"class":"resume-block__title-text resume-block__title-text_sub"}).find_all("span")[0].text[:2])*12+int(resume.find("span", attrs={"class":"resume-block__title-text resume-block__title-text_sub"}).find_all("span")[1].text[:2])
        elif len(resume.find("span", attrs={"class":"resume-block__title-text resume-block__title-text_sub"}).find_all("span")) == 1:
            experience = int(resume.find("span", attrs={"class": "resume-block__title-text resume-block__title-text_sub"}).find_all("span")[0].text[:2])
        else:
            experience = 0
        if resume.find("div", attrs={"class":"bloko-tag-list"}).find_all("div", attrs={"class":"bloko-tag bloko-tag_inline"}):
            skills = [i.text for i in resume.find("div", attrs={"class":"bloko-tag-list"}).find_all("div", attrs={"class":"bloko-tag bloko-tag_inline"})]
        else:
            skills = []
        if resume.find("div", attrs={"class":"resume-block-container", "data-qa":"resume-block-skills-content"}):
            about_me = resume.find("div", attrs={"class":"resume-block-container", "data-qa":"resume-block-skills-content"}).text
        else:
            about_me = None
        if resume.find("div", attrs={"data-qa":"resume-block-education"}).find("div", attrs={"class":"bloko-columns-row"}):
            education = resume.find("div", attrs={"data-qa":"resume-block-education"}).find("div", attrs={"class":"bloko-columns-row"}).text
        else:
            education = None
        if resume.find("div", attrs={"data-qa":"resume-block-languages"}).find("div", attrs={"class":"resume-block-item-gap"}).find_all("div", attrs={"class":"bloko-tag bloko-tag_inline"}):
            language = [i.text for i in resume.find("div", attrs={"data-qa":"resume-block-languages"}).find("div", attrs={"class":"resume-block-item-gap"}).find_all("div", attrs={"class":"bloko-tag bloko-tag_inline"})]
        else:
            language = []
        return language
    except Exception as e:
        print(f"Error: {e}")
        return 1, link


def get_links_vacancy(text):
    useragent = fake_useragent.UserAgent()

    def get_total_pages():
        data = requests.get(
            url=f"https://hh.ru/search/vacancy?text={text}&hhtmFrom=resume_search_result&hhtmFromLabel=vacancy_search_line",
            headers={"user-agent": useragent.random}
        )
        if data.status_code != 200:
            return 0
        soup = BeautifulSoup(data.content, "lxml")
        try:
            pages = int(
                soup.find(attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find("span").text)
            return pages
        except Exception as e:
            print(f"Error finding total pages: {e}")
            return 1

    total_pages = get_total_pages()

    for page in range(total_pages):
        data = requests.get(
            url=f"https://hh.ru/search/vacancy?text={text}&page={page}",
            headers={"user-agent": useragent.random}
        )
        if data.status_code != 200:
            continue
        soup = BeautifulSoup(data.content, features="lxml")
        for i in soup.find(attrs={"class": "vacancy-serp-content"}).find_all("div", attrs={"class": None}):
            h2_tag = i.find("h2", attrs={"data-qa": "bloko-header-2"})

            if h2_tag is not None:
                link = h2_tag.find("a")
                if link is not None:
                    yield "https://api." + f"{link.attrs['href'].split('?')[0]}".replace("vacancy", "vacancies", 1).split('.', 1)[1]

        time.sleep(1)
def get_vacancy(link):
    data = requests.get(url=link, headers={"user-agent":"Parser/1.0 (den.spesivtsev.006@gmail.com)"})
    if data.status_code != 200:
        return 0
    time.sleep(1)
    vacancy = data.json()
    name = vacancy.get("name")
    area = vacancy.get("area").get("name")
    if vacancy.get("salary"):
        salary_from = vacancy.get("salary").get("from")
        salary_to = vacancy.get("salary").get("to")
    experience = vacancy.get("experience").get("name")
    schedule = vacancy.get("schedule").get("name")
    employment = vacancy.get("employment").get("name")
    contacts = vacancy.get("contacts")
    description = BeautifulSoup(vacancy.get("description"),"lxml").text
    key_skills = [i.get("name") for i in vacancy.get("key_skills")]
    driver_license = [i.get("name") for i in vacancy.get("driver_license_types")]
    emloyer_name = vacancy.get("employer").get("name")
    languages = [i.get("name") for i in vacancy.get("languages")]
    return key_skills, link

if __name__ == "__main__":
    for page in get_links(None):
        print(get_resume(page))