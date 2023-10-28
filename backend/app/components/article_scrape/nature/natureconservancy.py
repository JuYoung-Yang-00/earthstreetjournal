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
import json

# Constants and global configurations
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT}
BASE_URL = "https://www.nature.org/en-us/what-we-do/our-insights/perspectives/"
MAX_ARTICLES = 20

session = requests.Session()
session.headers.update(HEADERS)

def scrape_natureconservancy():
    response = session.get(BASE_URL)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the hidden div containing the articleAggregationDetailsStr
    hidden_div_content = soup.select_one("span.articleAggregationDetailsStr").text
    article_data = json.loads(hidden_div_content)

    articles = []

    print(f"Found {len(article_data)} articles.")

    for idx, article_details in enumerate(article_data[:MAX_ARTICLES]):
        try:
            article_link = article_details['link']
            article = process_article(article_link)
            if article:
                articles.append(article)
                print(f"Processed article {idx + 1}.")
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



def process_article(article_link):
    try:
        article_response = session.get(article_link)
        # print(article_response.content.decode('utf-8'))
        
        article_soup = BeautifulSoup(article_response.content, 'html.parser')
        
        # Extract the required data from the provided HTML structure
        title = article_soup.select_one("h1.c-article-hero__title").text.strip()

        # Author information is found in the photo credit in the provided structure
        photo_credit = article_soup.select_one("p.c-article-hero__photo-credit").text.strip()
        author = photo_credit.split(",")[0].replace("By ", "").strip()  # Extract author's name
        
        date_string = article_soup.select_one("span.article-hero-article-date").text.strip()
        date_object = datetime.strptime(date_string, '%B %d, %Y')

        # Updated content_div selector to match the provided HTML structure
        content_divs = article_soup.select("div.article-row.bs_row p")
        # content_divs = article_soup.select("div.rte__text.c-rte.txt-clr-g1 p")
        content = ' '.join([p.text for p in content_divs])

        return {
            'category': 'nature',
            'title': title,
            'author': author,
            'source': 'natureconservancy',
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
