import requests
from bs4 import BeautifulSoup
import pandas as pd
import utils


def get_jobs(term):
    headers = {
        'User-Agent': utils.get_user_agent()
    }

    term = term.replace(" ", "-")
    job_list = []
    url = f"https://remoteok.com/remote-{term}-jobs"
    html_doc = requests.get(url, headers).text
    soup = BeautifulSoup(html_doc, "html.parser")
    tr_soup = soup.find_all("tr", {"class": "job"})
    print(html_doc)
    print(soup)
    for tr in tr_soup:
        title = tr.find("h2", {"itemprop": "title"}).text
        company = tr.get("data-company")
        link = "https://remoteok.com" + tr.get("data-href")
        job_list.append([title, company, link])

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

