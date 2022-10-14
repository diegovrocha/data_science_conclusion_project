import requests
from bs4 import BeautifulSoup
import pandas as pd
import utils


def get_jobs(term):
    term = term.replace(" ", "+")
    job_list = []
    url = f"https://weworkremotely.com/remote-jobs/search?term={term}"
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, "html.parser")
    list_article = soup.find_all("article")

    for article in list_article:
        list_item = article.find_all("li")

        for info in list_item:
            title = str(info.find("span", {"class": "title"}))
            title = title.replace('<span class="title">',
                                  '').replace('</span>', '')
            company = str(info.find("span", {"class": "company"}))
            company = company.replace(
                '<span class="company">', '').replace('</span>', '')
            link = "https://weworkremotely.com" + info.find("a").get("href")

            if title != 'None':
                job = {
                    "site": "weworkremotely.com",
                    "title": title,
                    "company": company,
                    "salary": "no info",
                    "summary": "no info",
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
