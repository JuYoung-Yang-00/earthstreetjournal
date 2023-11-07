# /app/components/article_scrape/scrape_routes.py

# For Scraping Articles from the Newspapers
from flask import Blueprint, jsonify, request

from ..article_scrape.politics import climatenews
from ..article_scrape.politics import eenews
from ..article_scrape.politics import politico

from ..article_scrape.nature import smithsonianmag
from ..article_scrape.nature import natureconservancy

from ..article_scrape.technology import techcrunch
from ..article_scrape.technology import theverge

from ..article_scrape.science import scientificamerican
from ..article_scrape.science import est
from ..article_scrape.science import sciencenews

import os
from dotenv import load_dotenv
load_dotenv()

scrape_bp = Blueprint('scrape', __name__)

@scrape_bp.route('/')
def index():
    return "Welcome to ESJ Scraping API!"

@scrape_bp.route('/<category>/<newspaper>')
def scrape(category, newspaper):
    articles = []
    if category == 'politics':
        if newspaper == 'climatenews':
            articles = climatenews.scrape_climatenews()
        elif newspaper == 'eenews':
            articles = eenews.scrape_eenews()
        elif newspaper == 'politico':
            articles = politico.scrape_politico()
    
    elif category == 'nature':
        if newspaper == 'smithsonianmag':
            articles = smithsonianmag.scrape_smithsonianmag()
        elif newspaper == 'natureconservancy':
            articles = natureconservancy.scrape_natureconservancy()
            
    elif category == 'technology':
        if newspaper == 'techcrunch':
            articles = techcrunch.scrape_techcrunch()
        # elif newspaper == 'theverge':
        #     articles = theverge.scrape_theverge()

    elif category =='science':
        # if newspaper =='scientificamerican':
        #     articles = scientificamerican.scrape_scientificamerican()
        if newspaper == 'est':
            articles = est.scrape_est()
        elif newspaper =='sciencenews':
            articles = sciencenews.scrape_sciencenews()

    return jsonify(articles)

scrape_all_key = os.getenv('SCRAPE_ALL_KEY')
@scrape_bp.route('/all/<string:scrape_all_key>')
def scrape_all(scrape_all_key):
    all_articles = []
    # Politics
    all_articles.extend(climatenews.scrape_climatenews())
    all_articles.extend(eenews.scrape_eenews())
    all_articles.extend(politico.scrape_politico())
    
    # Nature
    all_articles.extend(smithsonianmag.scrape_smithsonianmag())
    all_articles.extend(natureconservancy.scrape_natureconservancy())
    
    # Technology
    all_articles.extend(techcrunch.scrape_techcrunch())
    # The Verge scraping function is commented out and thus not included
    
    # Science
    # Scientific American scraping function is commented out and thus not included
    all_articles.extend(est.scrape_est())
    all_articles.extend(sciencenews.scrape_sciencenews())

    return jsonify(all_articles)
