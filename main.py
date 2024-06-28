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
        return personal_adress
    except Exception as e:
        print(f"Error finding total pages: {e}")
        return 1


if __name__ == "__main__":
    # Пример использования get_resume для одного резюме
    print(get_resume("https://hh.ru/resume/0de1b45d0008b61e070039ed1f6d6f4e4e4b43"))

