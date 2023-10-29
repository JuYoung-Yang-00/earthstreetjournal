"""
THIS IS A WORK IN PROGRESS. DO NOT USE THIS FILE.
COPIED FROM theverge.py -- only change name of function

"""





import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)
import random
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from app import mongo
import re

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT}
MAX_ARTICLES = 1
BASE_URL = 'https://www.theverge.com/environment'

session = requests.Session()
session.headers.update(HEADERS)

def get_article_links(base_url):
    session = requests.Session()
    response = session.get(base_url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    print(soup.prettify())
    
    
    article_links = [a['href'] for a in soup.select("h2.font-polysans.text-20.font-bold.leading-100.tracking-1.md.text-24 a")]

    return article_links


def scrape_est():
    article_links = ['https://www.theverge.com' + link for link in get_article_links(BASE_URL)]
    articles = []

    print(f"Found {len(article_links)} article links.")
    for idx, link in enumerate(article_links[:MAX_ARTICLES]):
        article = process_article(link)
        if article:
            articles.append(article)
            print(f"Processed article {idx + 1} successfully.")
            time.sleep(random.uniform(2, 5))
            
    store_in_mongodb(articles)
    print(f"Finished processing {len(articles)} articles.")
    return articles

def process_article(article_link):
    article_response = session.get(article_link)
    article_soup = BeautifulSoup(article_response.content, 'html.parser')
    # print(article_soup.prettify())

    title = article_soup.select_one("div.mb-24.grow h1.inline.font-polysans.text-22.font-bold.leading-110.md:text-33.lg:hidden").text.strip()
    author = article_soup.select_one("p.duet--article--article-byline span.font-medium a").text.strip()

    date_string_content = None

    # Date
    date_element = article_soup.select_one("div.duet--article--date-and-comments time.duet--article--timestamp")
    if date_element:
        datetime_string = date_element.get("datetime")
        match = re.search(r"\d{4}-\d{2}-\d{2}", datetime_string)
        if match:
            date_string_content = match.group()

    if not date_string_content:
        print(f"Failed to extract date string from time contents in article: {article_link}")
        return None
    date_object = datetime.strptime(date_string_content, "%Y-%m-%d")


    content = ' '.join([p.text for p in article_soup.select("div.duet--article--article-body-component-container p.duet--article--standard-paragraph")])

    return {
        'category': 'technology',
        'title': title,
        'author': author,
        'source': 'theverge',
        'content': content,
        'date': date_object,
        'link': article_link,
    }


def store_in_mongodb(data):
    inserted_ids = []
    for article in data:
        title = article.get('title')
        if not title:
            print("Article doesn't have a title. Skipping...")
            continue

        existing_article = mongo.db.articles.find_one({"title": title})
        if existing_article:
            print(f"Article with title '{title}' already exists. Skipping...")
            continue

        print(f"Inserting article titled '{title}'")
        result = mongo.db.articles.insert_one(article)
        inserted_ids.append(result.inserted_id)

    print(f"Successfully stored {len(inserted_ids)} articles in MongoDB.")

