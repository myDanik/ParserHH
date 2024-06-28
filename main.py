import requests
from bs4 import BeautifulSoup
import time
import fake_useragent



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
        resume = soup.find_all("div", attrs={"class":"bloko-columns-row"})[1]
        sex = resume.find("span", attrs={"data-qa":"resume-personal-gender"}).text
        age = int(resume.find("span", attrs={"data-qa":"resume-personal-age"}).text[:2])
        job_search_status = resume.find("div", attrs={"class": "resume-job-search-status"}).text
        personal_adress = resume.find("div", attrs={"class":"bloko-translate-guard"}).find("span",attrs={"data-qa": "resume-personal-address"}).text
        position = resume.find("div", attrs={"class":"resume-block-position"}).text
        specialization = resume.find("li", attrs={"class":"resume-block__specialization"}).text
        busyness = resume.find("div", attrs={"class":"resume-block-container"}).find_all("p")[0].text
        work_schedule = resume.find("div", attrs={"class":"resume-block-container"}).find_all("p")[1].text
        experience = int(resume.find("span", attrs={"class":"resume-block__title-text resume-block__title-text_sub"}).find_all("span")[0].text[:2])*12+int(resume.find("span", attrs={"class":"resume-block__title-text resume-block__title-text_sub"}).find_all("span")[1].text[:2])
        skills = [i.text for i in resume.find("div", attrs={"class":"bloko-tag-list"}).find_all("div", attrs={"class":"bloko-tag bloko-tag_inline"})]
        about_me = resume.find("div", attrs={"class":"resume-block-container", "data-qa":"resume-block-skills-content"}).text
        education = resume.find("div", attrs={"data-qa":"resume-block-education"}).find("div", attrs={"class":"bloko-columns-row"}).text
        language = [i.text for i in resume.find("div", attrs={"data-qa":"resume-block-languages"}).find("div", attrs={"class":"resume-block-item-gap"}).find_all("div", attrs={"class":"bloko-tag bloko-tag_inline"})]
    except Exception as e:
        print(f"Error finding total pages: {e}")
        return 1

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
                    yield f"{link.attrs['href'].split('?')[0]}"

        time.sleep(1)
def get_vacancy(link):
    pass

if __name__ == "__main__":
    for page in get_links_vacancy("python"):
        print(page)

