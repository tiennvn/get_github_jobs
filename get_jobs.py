#!/usr/bin/python3
import sqlite3
from bs4 import BeautifulSoup
import requests

base_url = 'https://github.com'
jobs_url = 'https://github.com/awesome-jobs/vietnam/issues?page='


def get_jobs():
    result = []
    for page in range(1, 12):
        html_data = requests.get(jobs_url + str(page)).text
        soup = BeautifulSoup(html_data, 'html.parser')
        jobs_page = soup.find_all('div', attrs={
            'class': 'float-left col-9 lh-condensed p-2'})
        for job in jobs_page:
            result.append((job.find('a').string.strip(),
                           base_url + job.find('a')['href'],
                           job.find('relative-time').string))
    return result


def create_jobs_db(jobs):
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE jobs
                 (job_name, job_url, job_time)''')
    for job in jobs:
        c.execute("INSERT INTO jobs VALUES(?, ?, ?)", job)
    conn.commit()
    conn.close()


def main():
    jobs = get_jobs()
    create_jobs_db(jobs)
    print('Done, open file jobs.db')


if __name__ == '__main__':
    main()
