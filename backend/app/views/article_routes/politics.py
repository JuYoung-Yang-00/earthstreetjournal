import requests
from bs4 import BeautifulSoup
import random
import time
from config import Config
from pymongo import MongoClient


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT}
MAX_ARTICLES = 50

session = requests.Session()
session.headers.update(HEADERS)

def scrape_politics():
    base_url = "https://insideclimatenews.org"
    category_url = f"{base_url}/category/politics-policy/"
    response = session.get(category_url)

    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    article_containers = soup.find_all('article')

    articles = []
    print(f"Found {len(article_containers)} article containers.")

    for idx, container in enumerate(article_containers[:MAX_ARTICLES]):
        try:
            link_container = container.find('a', href=True)
            article_link = link_container['href'] if link_container else None
            if not article_link:
                print(f"Article {idx + 1} link not found.")
                continue
            
            print(f"Identified article link {idx+1}: {article_link}")
            article = process_article(container)
            if article:
                articles.append(article)
                print(f"Appended article {idx + 1} to the list.")
                print(f"Current length of articles list: {len(articles)}")
                time.sleep(random.uniform(2, 5))
            else:
                print(f"Article {idx + 1} was identified but not processed successfully.")
                
        except Exception as e:
            print(f"Error processing article {idx + 1}. Reason: {str(e)}")
            with open("errors.log", "a") as log_file:
                log_file.write(f"Error processing article {idx + 1}. Reason: {str(e)}\n")
            continue

    print(f"Finished processing {len(articles)} articles.")
    return articles

def process_article(container):
    try:
        title_container = container.find('h2', class_='entry-title')
        subtitle_container = container.find('h2', class_='entry-subtitle')
        author_container = container.find('h3', class_='post-author')
        link_container = container.find('a', href=True)

        if link_container and title_container:
            title = title_container.text.strip()
            subtitle = subtitle_container.text.strip() if subtitle_container else None
            author = author_container.text.strip().replace("By ", "") if author_container else None
            link = link_container['href']
            
            content = get_article_content(link)
            
            return {
                'title': title,
                'subtitle': subtitle,
                'author': author,
                'link': link,
                'content': content,
            }
    except Exception as e:
        raise e
    return None

def get_article_content(url):
    print(f"Fetching content from {url}")
    response = session.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch content from {url}. Status code: {response.status_code}")
        return ""

    soup = BeautifulSoup(response.content, 'html.parser')
    content_container = soup.find('div', class_='entry-content')

    if content_container:
        return content_container.text.strip()
    else:
        print(f"Content not found for {url}. Looking for alternative content.")
        alternative_content = soup.find('article')
        return alternative_content.text.strip() if alternative_content else ""


def store_in_mongodb(data):
    try:
        # Use with statement for connection management
        with MongoClient(Config.MONGO_URI) as client:
            db = client['earthstreetjournal']

            inserted_ids = []
            for article in data:
                # Ensure each article is a dictionary
                if not isinstance(article, dict):
                    print(f"Skipped invalid article data: {article}")
                    continue

                try:
                    print(f"Trying to insert article titled '{article.get('title', 'No Title')}'")
                    result = db.articles.insert_one(article)
                    inserted_ids.append(result.inserted_id)
                except Exception as indv_exc:
                    print(f"Error inserting article titled '{article.get('title', 'No Title')}'. Reason: {indv_exc}")

            print(f"Inserted IDs: {inserted_ids}")
            print(f"Successfully stored {len(inserted_ids)} articles in MongoDB.")

    except Exception as e:
        print(f"Error connecting to MongoDB or processing data. General reason: {e}")



        
if __name__ == "__main__":
    articles = scrape_politics()
    if articles:
        store_in_mongodb(articles)  
        for idx, article in enumerate(articles):
            print(f"Processing article {idx + 1}: {article['title']}")
            print(article)
    else:
        print("No articles were scraped.")



