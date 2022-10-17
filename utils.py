import os
import csv
from bs4 import BeautifulSoup
from http import HTTPStatus
import requests
import random

MAIN_DIR = os.path.dirname(os.path.realpath(__file__))
CSV_PATH = MAIN_DIR + '/jobs.csv'

def write_csv(job_list):
    isExist = os.path.exists(CSV_PATH)

    with open(CSV_PATH, "a", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=['site', 'title', 'company', 'salary', 'summary', 'link'], delimiter=';')

        if not isExist:
            writer.writeheader()
        writer.writerows(job_list)

def get_user_agent():
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    ]
    user_agent = random.choice(user_agent_list)
    return user_agent

def test_site(site):
    try:
        url = site
        headers = {
                'user-agent': get_user_agent()
        }

        response = requests.get(url, headers)
        html_doc = response.text
        soup = BeautifulSoup(html_doc, "html.parser")
        print(f'Response status: {response.status_code}, {HTTPStatus(response.status_code).phrase}')
        
        arquivo = MAIN_DIR + '/html/' + site.split('/')[2] + '.html'
        with open(arquivo, 'w') as file:
            file.write(str(soup))

        if response.status_code != HTTPStatus.OK:
            raise Exception(
                f'Erro ao acessar o site {url}, retorno {response.status_code}-{HTTPStatus(response.status_code).phrase}')
    except Exception as error:
        print('Ocorreu um erro: ' + error.args[0])

