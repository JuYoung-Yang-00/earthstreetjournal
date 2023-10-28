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

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT}
MAX_ARTICLES = 50

BASE_URL = 'https://www.smithsonianmag.com/category/science-nature/'

session = requests.Session()
session.headers.update(HEADERS)


def get_article_links(base_url):
    response = session.get(base_url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    article_links = [a['href'] for a in soup.select("div.article-list-text h3 a")]
    # Add the base domain to each relative URL
    full_links = ['https://www.smithsonianmag.com' + link for link in article_links]
    return full_links

def scrape_smithsonianmag():
    article_links = get_article_links(BASE_URL)
    articles = []
    print(f"Found {len(article_links)} article links.")
    
    for idx, link in enumerate(article_links[:MAX_ARTICLES]):
        try:
            article = process_article(link)
            if article:
                articles.append(article)
                print(f"Processed article {idx + 1} successfully.")
                time.sleep(random.uniform(2, 5))
            else:
                print(f"Article {idx + 1} was not processed successfully.")
        except Exception as e:
            print(f"Error processing article {idx + 1}. Reason: {str(e)}")
            
    store_in_mongodb(articles)
    print(f"Finished processing {len(articles)} articles.")
    return articles

def process_article(article_link):
    try:
        article_response = session.get(article_link)
        article_soup = BeautifulSoup(article_response.content, 'html.parser')
        
        title = article_soup.select_one("h1.headline").text.strip()
        author = article_soup.select_one("div.author-text p.author a").text.strip()
        date_string = article_soup.select_one("time.pub-date").text.strip()
        date_object = datetime.strptime(date_string, '%B %d, %Y')
        
        # Correct the selector to target the p tags inside the div with data-article-body attribute
        content_divs = article_soup.select("div.articleLeft[data-article-body] p")
        content = ' '.join([p.text for p in content_divs])

        return {
            'category': 'nature',
            'title': title,
            'author': author,
            'source': 'smithsonianmag',
            'content': content,
            'date': date_object,
            'link': article_link,
        }
    except Exception as e:
        raise e
    return None

def store_in_mongodb(data):
    try:
        inserted_ids = []
        for article in data:
            if not isinstance(article, dict):
                print(f"Skipped invalid article data: {article}")
                continue
            title = article.get('title')
            if not title:
                print("Article doesn't have a title. Skipping...")
                continue
            existing_article = mongo.db.articles.find_one({"title": title})
            if existing_article:
                print(f"Article with title '{title}' already exists. Skipping...")
                continue
            try:
                print(f"Inserting article titled '{title}'")
                result = mongo.db.articles.insert_one(article)
                inserted_ids.append(result.inserted_id)
            except Exception as indv_exc:
                print(f"Error inserting article titled '{title}'. Reason: {indv_exc}")
        print(f"Inserted IDs: {inserted_ids}")
        print(f"Successfully stored {len(inserted_ids)} articles in MongoDB.")
    except Exception as e:
        print(f"Error connecting to MongoDB or processing data. General reason: {e}")






