import requests
from bs4 import BeautifulSoup
import pandas as pd
import utils


def get_jobs(term):
    term = term.replace(" ", "+")
    job_list = []
    url = f"https://www.flexjobs.com/search?search={term}"
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, "html.parser")
    list_jobs = soup.find_all("ul", {"id": "job-list"})

    for job_item in list_jobs:
        li_list = job_item.find_all("li")
        for li in li_list:
            title = li.find("a", {"class": "job-title"}).text
            title = title.replace('\n', '')
            
            summary = li.find("div", {"class": "job-description"}).text
            summary = summary.replace('\n', '')
            
            link = 'https://www.flexjobs.com'+li.find("a").get("href")
            link = link.replace('\n', '')

            if title != 'None':
                job = {
                    "site": "flexjobs.com",
                    "title": title.strip(),
                    "company": "no info",
                    "salary": "no info",
                    "summary": summary.strip(),
                    "link": link
                }
                job_list.append(job)

    return job_list


if __name__ == "__main__":
    # Job Roles in Data Science
    roles = ['data analyst', 'data engineers',
             'machine learning engineer', 'data scientist', 'data architect']

    for role in roles:
        job_list = get_jobs(role)
        df = pd.DataFrame(job_list)
        utils.write_csv(job_list)
        print(df)

