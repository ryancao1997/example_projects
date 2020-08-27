from bs4 import BeautifulSoup
import requests
from lxml import html
import csv, os, json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(ChromeDriverManager().install())
URL = 'https://www.wsj.com/news/business/health-industry'
browser.get(URL)
soup = BeautifulSoup(browser.page_source, 'html.parser')
articles = soup.find_all('article')


article_data = []
for article in articles:
    title_div = str(article.find('div', class_ = 'WSJTheme--headline--7VCzo7Ay '))
    title = title_div.split('>')[3].split('<')[0]
    href = title_div.split('href=')[1].split('>')[0]
    date = str(article.find('p', class_ = 'WSJTheme--timestamp--22sfkNDv ')).split('>')[1].split('<')[0]
    summary = str(article.find('p', class_ = 'WSJTheme--summary--lmOXEsbN ')).split('>')[1].split('<')[0]
    authors = str(article.find('p', class_ = 'WSJTheme--byline--1oIUvtQ3 ')).split('>')[1].split('<')[0]
    article_info = {}
    article_info['title'] = title
    article_info['summary'] = summary
    article_info['authors'] = authors
    article_info['date'] = date
    article_info['href'] = href
    article_data.append(article_info)

print(article_data)