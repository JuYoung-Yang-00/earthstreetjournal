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
MAX_ARTICLES = 50
BASE_URL = 'https://techcrunch.com/category/climate/'

session = requests.Session()
session.headers.update(HEADERS)

def get_article_links(base_url):
    response = session.get(base_url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    article_links = [a['href'] for a in soup.select("h2.post-block__title a")]
    return article_links

def scrape_techcrunch():
    article_links = get_article_links(BASE_URL)
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

    title = article_soup.select_one("div.article__title-wrapper h1.article__title").text.strip()
    
    author_element = article_soup.find('div', class_='article__byline')

        # Check if the element was found and extract authors
    if author_element:
        # Extracting all 'a' tags which contain the author names
        author_tags = author_element.find_all('a')

        # Extracting the text from these 'a' tags (the author names) and joining them
        authors = ' and '.join(author.text.strip() for author in author_tags)
    else:
        authors = "nope"
    print(authors)
    

    #author = article_soup.select_one("div.article__byline a").text.strip()

    date_string_content = None

    # First try to extract date from the HTML content
    date_element = article_soup.select_one("div.article__byline-wrapper time.full-date-time")
    if date_element:
        time_contents = date_element.get_text()
        match = re.search(r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},\s\d{4}\b", time_contents)
        if match:
            date_string_content = match.group()

    # If above method failed, try extracting from JavaScript content
    if not date_string_content:
        scripts = article_soup.find_all('script')
        for script in scripts:
            if 'var tc_app_data' in script.text:
                match = re.search(r'"date":"(.*?)T', script.text)
                if match:
                    date_string_content = match.group(1)
                    break

    # If still not found, return an error
    if not date_string_content:
        print(f"Failed to extract date string from time contents in article: {article_link}")
        return None

    # Convert the date string into a datetime object
    date_object = datetime.strptime(date_string_content, "%Y-%m-%d")

    content = ' '.join([p.text for p in article_soup.select("div.article-content p")])

    return {
        'category': 'technology',
        'title': title,
        'author': authors,
        'source': 'techcrunch',
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

