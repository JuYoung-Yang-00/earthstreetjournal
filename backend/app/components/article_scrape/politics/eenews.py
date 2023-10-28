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
from app import mongo

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT}
MAX_ARTICLES = 50

session = requests.Session()
session.headers.update(HEADERS)

def scrape_eenews():
    base_url = 'https://www.eenews.net'
    response = session.get(base_url)

    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    
    recent_stories_header = soup.find(string="Explore Recent Stories")
    
    if not recent_stories_header:
        print("Failed to locate 'Explore Recent Stories' section.")
        return []
    
    article_containers = []
    for sibling in recent_stories_header.find_all_next():
        if sibling.name == 'div' and 'main-post-list' in sibling.get('class', []):
            article_containers.append(sibling)
        if len(article_containers) >= MAX_ARTICLES:
            break

    articles = []
    print(f"Found {len(article_containers)} article containers in 'Explore Recent Stories'.")

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
        if link_container:
            if link_container['href'].startswith(('http', 'https')):
                article_link = link_container['href']
            else:
                article_link = base_url + link_container['href']
            
            article_response = session.get(article_link)
            article_soup = BeautifulSoup(article_response.content, 'html.parser')

            title = article_soup.find('h1').text.strip() if article_soup.find('h1') else None
            subtitle = article_soup.find('h2').text.strip() if article_soup.find('h2') else None
            author = article_soup.find('strong').text.strip() if article_soup.find('strong') else None
            content_div = article_soup.find('div', class_='entry-content')
            content = " ".join([p.text.strip() for p in content_div.find_all('p')]) if content_div else None
            
            date_object = None
            date_element = article_soup.find('p')
            if date_element:
                date_parts = date_element.text.split('|')
                if len(date_parts) > 1:
                    date_string = date_parts[1].strip().split()[0]
                    date_object = datetime.strptime(date_string, '%m/%d/%Y')
                
            return {
                'category': 'politics',
                'title': title,
                'author': author,
                'source' : 'eenews',
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


