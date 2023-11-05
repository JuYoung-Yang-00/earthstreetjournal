# app/components/summarized/routes.py
from flask import Blueprint, jsonify, request
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from app import mongo

summarized_bp = Blueprint('summarized', __name__)

@summarized_bp.route('/<string:category>', methods=['GET'])
def get_summarized_articles_by_category(category):
    try:
        valid_categories = ["politics", "nature", "technology", "science"]
        if category not in valid_categories:
            return jsonify({'error': 'Invalid category specified'}), 400
        
        articles = mongo.db.summaries.find({'category': category})

        summarized_articles = list(articles)
        for article in summarized_articles:
            article['_id'] = str(article['_id'])

        return jsonify(summarized_articles), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500