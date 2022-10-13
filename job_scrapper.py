from bs4 import BeautifulSoup
from http import HTTPStatus
import requests
import csv
import pandas as pd
import random
import os

main_dir = os.path.dirname(os.path.realpath(__file__))

def get_user_agent():
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    ]
    user_agent = random.choice(user_agent_list)
    return user_agent


def get_remoteok_jobs(term):
    headers = {
        'User-Agent': get_user_agent()
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

def get_indeed_jobs():
    url = "https://search.indeed.jobs/main/jobs?keywords=java&sortBy=relevance&page=1"
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, "html.parser")
    job_list = soup.find_all('job-results-container')

    print(len(job_list))
    print(job_list)

def get_weworkremotely_jobs(term):
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
                    "salary": "no salary info",
                    "link": link,
                    "summary": ""
                }
                job_list.append(job)

    return job_list

def get_flexjobs_jobs(term):
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
            company = ''
            
            summary = li.find("div", {"class": "job-description"}).text
            summary = summary.replace('\n', '')
            
            link = 'https://www.flexjobs.com'+li.find("a").get("href")
            link = link.replace('\n', '')

            if title != 'None':
                job = {
                    "site": "flexjobs.com",
                    "title": title,
                    "company": company,
                    "salary": "no salary info",
                    "link": link,
                    "summary": summary
                }
                job_list.append(job)

    return job_list

def test_site(site):
    try:
        url = site
        headers = {
                ':authority':'remoteok.com',
                ':method': 'GET',
                ':path': '/?tags=java&action=get_jobs&offset=20',
                ':scheme':'https',
                'accept': '*/*',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'en-US,en;q=0.9,pt;q=0.8',
                'cookie':'ref=https%3A%2F%2Fremoteok.com%2F; new_user=false; adShuffler=1; visits=7; visit_count=7',
                'referer':'https://remoteok.com/remote-java-jobs',
                'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
                'sec-ch-ua-mobile':'?0',
                'sec-ch-ua-platform':'"macOS"',
                'sec-fetch-dest':'empty',
		        'sec-fetch-mode':'cors',
                'sec-fetch-site': 'same-origin',
                #'user-agent': get_user_agent,
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest'                
        }

        response = requests.get(url)
        html_doc = response.text
        soup = BeautifulSoup(html_doc, "html.parser")
        #print(f'Response status: {response.status_code}, {HTTPStatus(response.status_code).phrase}')
        
        arquivo = main_dir + '/html/' + site.split('/')[2] + '.html'
        with open(arquivo, 'w') as file:
            file.write(str(soup))

        if response.status_code != HTTPStatus.OK:
            raise Exception(
                f'Erro ao acessar o site {url}, retorno {response.status_code}-{HTTPStatus(response.status_code).phrase}')
    except Exception as error:
        print('Ocorreu um erro: ' + error.args[0])

def write_csv(job_list):
    jobs_csv = main_dir + '/jobs.csv'
    isExist = os.path.exists(jobs_csv)

    with open(jobs_csv, "a") as file:
        writer = csv.DictWriter(
            file, fieldnames=['site', 'title', 'company', 'salary', 'link', 'summary'])

        if not isExist:
            writer.writeheader()
        writer.writerows(job_list)


if __name__ == "__main__":
    # Job Roles in Data Science
    roles = ['data analyst','data engineers','machine learning engineer','data scientist','data architect']
    
    for role in roles:
        job_list = get_weworkremotely_jobs(role)
        write_csv(job_list)
        job_list = get_flexjobs_jobs(role)
        write_csv(job_list)
    
    '''
    title = 'data analyst'
    job_list = get_weworkremotely_jobs(title)
    write_csv(job_list)
    df = pd.DataFrame(job_list)
    print(df)

    job_list = get_flexjobs_jobs(title)
    write_csv(job_list)
    df = pd.DataFrame(job_list)
    print(df)
    '''
    #test_site('https://remoteok.com/?tags=java&action=get_jobs&offset=20')
