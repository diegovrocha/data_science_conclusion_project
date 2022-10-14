import requests
from bs4 import BeautifulSoup
import pandas as pd
import utils


def get_jobs(term):
    try:
        headers = {
            'authority': 'dd.angel.co',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,pt;q=0.8',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://angel.co',
            'referer': 'https://angel.co/',
            'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }
        term = term.replace(" ", "+")

        url = site
        response = requests.post(url, headers=headers)
        html_doc = response.text
        soup = BeautifulSoup(html_doc, "html.parser")
        #job_list = soup.find_all("script", {"id": "__NEXT_DATA__"})
        print(soup)
        '''
        for job in job_list:
            li_list = job.find_all("li")
            for li in li_list:
                title = li.find("div", {"class": "row"}).text
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
                    jobs.append(job)
        '''

        main_dir = os.path.dirname(os.path.realpath(__file__))
        arquivo = main_dir + '/html/' + site.split('/')[2] + '.html'
        with open(arquivo, 'w') as file:
            file.write(str(soup))

        if response.status_code != HTTPStatus.OK:
            raise Exception(
                f'Erro ao acessar o site {url}, retorno {response.status_code}-{HTTPStatus(response.status_code).phrase}')

        df = pd.DataFrame(jobs)
        print(df)
    except Exception as error:
        print('Ocorreu um erro: ' + error.args[0])



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

