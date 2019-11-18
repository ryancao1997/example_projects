#This script only runs if you create a new one column csv with just company names in the column and call this file  'test.csv' and a empty csv called 'company_sizes.csv'.
from bs4 import BeautifulSoup
import requests
import csv
import clarus
from lxml import html
import csv, os, json
import requests
import pandas as pd
from time import sleep

#establishes linkedin connection
HOMEPAGE_URL = 'https://www.linkedin.com'
LOGIN_URL = 'https://www.linkedin.com/uas/login-submit'
client = requests.Session()
html = client.get(HOMEPAGE_URL).content
soup = BeautifulSoup(html)
csrf = soup.find(id="loginCsrfParam-login")['value']
email = ''
password = ''

login_information = {
    'session_key':email,
    'session_password':password,
    'loginCsrfParam': csrf,
}


client.post(LOGIN_URL, data=login_information)
headers = {'Accept-Encoding': 'identity'}


#reads in file containing only company names, please change test.csv to the csv contating only company names that you created
csv = clarus.read_csv('test.csv')
companies = []
for row in csv:
    companies.append(row[0])

rows = [['Company', 'Linkedin URL', 'Company Size']]
#iterates through list of companies to get company size
not_founds = 0
for company in companies:
    company_ = company.replace(" ", "-")
    company_ = company_.replace('-Inc','')
    company_ = company_.replace(',', '')
    company_ = company_.replace('.', '')
    print(company)
    url = 'https://www.linkedin.com/company/'+company_+'/insights'
    try:
        company_url = client.get(url, headers=headers)
        soup = BeautifulSoup(company_url.content)
        soup = soup.text
        split = soup.split('"totalEmployees":')[1]
        split2 = split.split(',"headcounts"')[0]
        info = split2
        company_size = info
    except:
        company_size = 'Not Found'
        not_founds += 1
        url = 'Not Found'
    print(company_size)
    rows.append([company, url, company_size])


#please replace the filename of a blank csv that you saved on your working directory
filename = 'company_sizes.csv'

#wrties csv file containing answers
my_df = pd.DataFrame(rows)
print(my_df)
my_df.to_csv(filename, index=False, header=True)

