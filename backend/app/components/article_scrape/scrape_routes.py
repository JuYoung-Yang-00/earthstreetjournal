# routes.py

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

scrape_bp = Blueprint('scrape', __name__)

@scrape_bp.route('/')
def index():
    return "Welcome to Earth Street Journal Scraping API!"

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
        elif newspaper == 'theverge':
            articles = theverge.scrape_theverge()

    elif category =='science':
        if newspaper =='scientificamerican':
            articles = scientificamerican.scrape_scientificamerican()
        elif newspaper == 'est':
            articles = est.scrape_est()
        elif newspaper =='sciencenews':
            articles = sciencenews.scrape_sciencenews()

    return jsonify(articles)

