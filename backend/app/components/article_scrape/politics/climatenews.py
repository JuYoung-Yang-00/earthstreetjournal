import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)
import requests
from bs4 import BeautifulSoup
import random
import time
from datetime import datetime
from urllib.parse import urljoin
from app import mongo


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT}
MAX_ARTICLES = 50

session = requests.Session()
session.headers.update(HEADERS)
 
def scrape_climatenews():
    base_url = "https://insideclimatenews.org"
    category_url = f"{base_url}/category/politics-policy/"
    response = session.get(category_url)

    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    article_containers = soup.find_all('article', limit=MAX_ARTICLES)

    articles = []
    print(f"Found {len(article_containers)} article containers.")

    for idx, container in enumerate(article_containers):
        try:
            article = process_article(container, base_url)
            if article:
                articles.append(article)
                print(f"Appended article {idx + 1} to the list.")
                time.sleep(random.uniform(2, 5))
            else:
                print(f"Article {idx + 1} was not processed successfully.")
        except Exception as e:
            print(f"Error processing article {idx + 1}. Reason: {str(e)}")
            with open("errors.log", "a") as log_file:
                log_file.write(f"Error processing article {idx + 1}. Reason: {str(e)}\n")

    store_in_mongodb(articles) 
    print(f"Finished processing {len(articles)} articles.")
    return articles

def process_article(container, base_url):
    try:
        link_container = container.find('a', href=True)
        article_link = urljoin(base_url, link_container['href']) if link_container else None

        if not article_link:
            print("No link found for article")
            return None

        article_response = session.get(article_link)
        article_soup = BeautifulSoup(article_response.content, 'html.parser')

        title = article_soup.find('h1').text.strip() if article_soup.find('h1') else None
        subtitle = article_soup.find('h2').text.strip() if article_soup.find('h2') else None
        author = article_soup.find('h3', class_='post-author').text.strip().replace("By ", "") if article_soup.find('h3', class_='post-author') else None
        content_div = article_soup.find('div', class_='entry-content')
        content = " ".join([p.text.strip() for p in content_div.find_all('p')]) if content_div else None

        date_element = article_soup.find('meta', property="article:published_time")
        date_object = datetime.fromisoformat(date_element['content']) if date_element else None

        return {
            'category': 'politics',
            'title': title,
            'author': author,
            'source' : 'climatenews',
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

            # Check if the article with the given title already exists
            existing_article = mongo.db.articles.find_one({"title": title})
            if existing_article:
                print(f"Article with title '{title}' already exists. Skipping...")
                continue

            try:
                print(f"Trying to insert article titled '{title}'")
                result = mongo.db.articles.insert_one(article)
                inserted_ids.append(result.inserted_id)
            except Exception as indv_exc:
                # This exception will also catch attempts to insert a duplicate title due to the unique index
                print(f"Error inserting article titled '{title}'. Reason: {indv_exc}")

        print(f"Inserted IDs: {inserted_ids}")
        print(f"Successfully stored {len(inserted_ids)} articles in MongoDB.")

    except Exception as e:
        print(f"Error connecting to MongoDB or processing data. General reason: {e}")

