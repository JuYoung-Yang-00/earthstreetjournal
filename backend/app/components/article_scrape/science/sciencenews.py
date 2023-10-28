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

def scrape_sciencenews():
    base_url = "https://www.sciencenews.org"
    category_url = f"{base_url}/topic/climate"
    response = session.get(category_url)

    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []
    else:
        print(response.status_code)

    soup = BeautifulSoup(response.content, 'html.parser')
    ## FROM HERE SHIT WILL BE DIFF
    ##10.27.2023 (fri) 7pm
    # called li for the sciencenews
    #article_containers = soup.find_all('article', limit=MAX_ARTICLES)
    article_containers = soup.find_all('li', class_='post-item-river__wrapper___Nv-Ol with-image', limit=MAX_ARTICLES)
    print(len(article_containers))
    # cleared till here
    articles = []
    print(f"Found {len(article_containers)} article containers.")

    for idx, container in enumerate(article_containers):
        try:
            article = process_sciencenews_article(container, base_url)
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
    
    # store_in_mongodb(articles)
    print(f"Finished processing {len(articles)} articles.")
    return articles

def process_sciencenews_article(container, base_url):
    try:
        link_container = container.find('a', href=True)
        article_link = urljoin(base_url, link_container['href']) if link_container else None
        print(article_link)

        if not article_link:
            print("No link found for article")
            return None

        article_response = session.get(article_link)
        article_soup = BeautifulSoup(article_response.content, 'html.parser')

        
        title_element = article_soup.find('h1', class_='header-default__title___ychM4')
        title = title_element.text.strip() if title_element else None
        #print(title)

        #subtitle = article_soup.find('h2').text.strip() if article_soup.find('h2') else None
        #author = article_soup.find('h3', class_='post-author').text.strip().replace("By ", "") if article_soup.find('h3', class_='post-author') else None
        
        # Find the 'p' tag with the class 'story-meta__authors'
        author_element = article_soup.find('span', class_='byline author vcard')

        # Check if the element was found and extract authors
        if author_element:
            # Extracting all 'a' tags which contain the author names
            author_tags = author_element.find_all('a')
    
            # Extracting the text from these 'a' tags (the author names) and joining them
            authors = ' and '.join(author.text.strip() for author in author_tags)
        else:
            authors = "nope"
        print(authors)
        '''
        else:
            article_authors = article_soup.find('div', class_='article-meta__authors')
            if article_authors:
                authors_tags = article_authors.find_all('a')
                authors = ' and '.join(author.get_text() for author in authors_tags)
        '''
        sections = article_soup.find_all('div', class_='rich-text rich-text--with-sidebar single__rich-text___RmCDp')
        # We'll store all the paragraph texts in this list.
        all_paragraphs_text = []

        # Iterate through each found section and extract the text from the paragraphs.
        for section in sections:
            # Find all paragraphs in this section with the class "story-text__paragraph"
            paragraphs = section.find_all('p')
            
            section_text = ' '.join(para.text.strip() for para in paragraphs)
            all_paragraphs_text.append(section_text)

        # Join all the paragraph texts together into one string.
        content = ' '.join(all_paragraphs_text)


        date_element = article_soup.find('time', {'datetime': True})
        date_str = None
        date_object = None

        if date_element:
            date_str = date_element.get('datetime')
            if date_str:
                try: 
                    date_format = "%Y-%m-%dT%H:%M:%S%z"  # Note the 'T' separator and timezone (%z)
                    date_object = datetime.strptime(date_str, date_format)
                except ValueError as e:
                    print(f"Error parsing date string {date_str}: {e}")

        if authors == "" or authors == "nope":
            return None
        else:
            return {
                'category': 'science',
                'title': title,
                'author': authors,
                'source' : 'sciencenews',
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