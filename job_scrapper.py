from bs4 import BeautifulSoup
import requests
import pandas as pd
import utils
import worker_jobspresso
import worker_flexjobs
import worker_weworkremotely


def get_remoteok_jobs(term):
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

    job_list = []
    for role in roles:
        job_list = worker_weworkremotely.get_jobs(role)
        utils.write_csv(job_list)

        job_list = worker_flexjobs.get_jobs(role)
        utils.write_csv(job_list)

        job_list = worker_jobspresso.get_jobs(role)
        utils.write_csv(job_list)

        '''
        df = pd.DataFrame(job_list)
        print(df)
        write_csv(job_list)
        '''

    # test_site('https://remoteok.com/?tags=java&action=get_jobs&offset=20')
