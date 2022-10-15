from bs4 import BeautifulSoup
import requests
import pandas as pd
import utils
import worker_jobspresso
import worker_flexjobs
import worker_weworkremotely

if __name__ == "__main__":
    # Job Roles in Data Science
    roles = ['data analyst', 'data engineers',
             'machine learning engineer', 'data scientist', 'data architect']
    '''
    job_list = []
    for role in roles:
        job_list = worker_weworkremotely.get_jobs(role)
        utils.write_csv(job_list)

        job_list = worker_flexjobs.get_jobs(role)
        utils.write_csv(job_list)

        job_list = worker_jobspresso.get_jobs(role)
        utils.write_csv(job_list)
        
        df = pd.DataFrame(job_list)
        print(df)
        write_csv(job_list)
    '''

    utils.test_site('https://br.indeed.com/?r=us')
