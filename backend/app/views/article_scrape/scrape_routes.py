# routes.py

# For Scraping Articles from the Newspapers
from flask import Blueprint, jsonify, request
from ..article_scrape.nature import nature
from ..article_scrape.politics import climatenews
from ..article_scrape.politics import eenews
from ..article_scrape.technology import tech

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
        if newspaper == 'eenews':
            articles = eenews.scrape_eenews()
    elif category == 'tech':
        articles = tech.scrape_tech()
    elif category == 'nature':
        articles = nature.scrape_nature()
    return jsonify(articles)

