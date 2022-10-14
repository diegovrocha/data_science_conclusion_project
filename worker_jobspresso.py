import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import utils


def get_jobs(term):
    cookies = {
        'tk_or': '%22https%3A%2F%2Fblog.dsacademy.com.br%2F%22',
        'tk_r3d': '%22https%3A%2F%2Fblog.dsacademy.com.br%2F%22',
        'tk_lr': '%22https%3A%2F%2Fblog.dsacademy.com.br%2F%22',
        '_ga': 'GA1.2.233840706.1665625327',
        '_gid': 'GA1.2.1265934500.1665625327',
    }

    headers = {
        'authority': 'jobspresso.co',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,pt;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'tk_or=%22https%3A%2F%2Fblog.dsacademy.com.br%2F%22; tk_r3d=%22https%3A%2F%2Fblog.dsacademy.com.br%2F%22; tk_lr=%22https%3A%2F%2Fblog.dsacademy.com.br%2F%22; _ga=GA1.2.233840706.1665625327; _gid=GA1.2.1265934500.1665625327',
        'origin': 'https://jobspresso.co',
        'referer': 'https://jobspresso.co/remote-work/',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    term_aux = term.split(' ')
    term_search = ''
    if len(term_aux) > 1:
        term_search = term_aux[0] + '&20' + term_aux[1]
    else:
        term_search = term_aux

    term_search = 'search_keywords=' + term_search + \
        '&search_location=&filter_job_type%5B%5D=developer&filter_job_type%5B%5D=devops&filter_job_type%5B%5D='

    data = {
        'lang': '',
        'search_keywords': term,
        'search_location': '',
        'filter_job_type[]': [
            'developer',
            'devops',
            '',
        ],
        'per_page': '30',
        'orderby': 'featured',
        'order': 'DESC',
        'page': '1',
        'show_pagination': 'false',
        'form_data': term_search
    }

    response = requests.post('https://jobspresso.co/jm-ajax/get_listings/',
                             cookies=cookies, headers=headers, data=data)
    list_jobs = json.loads(response.content)
    soup = BeautifulSoup(list_jobs['html'], "html.parser")
    list_jobs = soup.find_all("li", {"class": "job_listing"})
    job_list = []

    for job in list_jobs:
        title = job.find("h3", {"class": "job_listing-title"}).text
        company = job.find(
            "div", {"class": "job_listing-company"}).select("strong")[0].text
        link = job.get("data-href")

        headers = {
            'authority': 'www.google-analytics.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,pt;q=0.8',
            # 'content-length': '0',
            'content-type': 'text/plain',
            'origin': 'https://jobspresso.co',
            'referer': link,
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }

        responseSummary = requests.post(link, headers=headers)
        soupSummary = BeautifulSoup(responseSummary.text, "html.parser")
        job_listing_description = soupSummary.find_all(
            "div", {"class": "job_listing-description"})

        job_summary = ""
        for item_job in job_listing_description:
            job_summary += item_job.text + " "
        
        if title != 'None':
            job = {
                    "site": "jobspresso.com",
                    "title": title,
                    "company": company,
                    "salary": "no info",
                    "summary": job_summary,
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

