# routes.py

from flask import Blueprint, jsonify, request
from .article_routes import politics, tech, nature

route_bp = Blueprint('routes', __name__)

@route_bp.route('/')
def index():
    return "Welcome to Earth Street Journal API!"

@route_bp.route('/scrape/<category>')
def scrape(category):
    articles = []
    if category == 'politics':
        articles = politics.scrape_politics()
    elif category == 'tech':
        articles = tech.scrape_tech()
    elif category == 'nature':
        articles = nature.scrape_nature()
    return jsonify(articles)

