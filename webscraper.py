# Basic webscraper with BeautifulSoup to pull dates and titles of blog posts from a publicly available site.

import requests

from bs4 import BeautifulSoup

import datetime

url = "https://pixelford.com/blog/"

import random

random_number = random.randint(1,99999999)

response = requests.get(url, headers = {'user-agent': f'Hi {random_number}'})
html = response.content

soup = BeautifulSoup(html, 'html.parser')

blogs = soup.find_all('article', class_="type-post")

for blog in blogs: 
    title = blog.find('a', class_="entry-title-link").get_text()
    time_tag = blog.find('time', class_="entry-time").get('datetime')
    blog_datetime = datetime.datetime.fromisoformat(time_tag)
    clean_date = blog_datetime.strftime("%A %B %m %H")
    print(f"{clean_date} - {title}")

# for a_tag in a_tags:
#     print(a_tag.get_text())

# titles = list(map(lambda a_tag: a_tag.get_text(), a_tags))

# print(titles)