# app/components/summaries/routes.py
import os
import sys
import json
from flask import Blueprint, jsonify
from bson import ObjectId, json_util
from datetime import datetime
from app import mongo
from config import Config
from app.components.summarize.summarize import OpenAISummarizer

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

summary_bp = Blueprint('summary', __name__)

# Helper function to get the latest article_id from summaries collection
def get_latest_article_id_from_summaries():
    latest_summary = mongo.db.summaries.find_one(sort=[('_id', -1)])  # Sort by descending _id to get the latest
    if latest_summary:
        return latest_summary['_id']
    return None

def insert_summary_into_summaries(article_id, title, summary, category, author, source, date):
    mongo.db.summaries.insert_one({
        '_id': article_id,
        'category': category,
        'title': title,
        'summary': summary,
        'author': author,
        'source': source,
        'date': date
    })
 
  
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

@summary_bp.route('/summarize-article', methods=['GET'])
def summarize_article():
    try:
        summarizer = OpenAISummarizer(Config.OPENAI_API_KEY)

        # Check if summary already exists for the article
        summarized_article_ids = [summary['_id'] for summary in mongo.db.summaries.find({}, {"_id": 1})]
        article_to_summarize = None
        query = {'_id': {'$nin': summarized_article_ids}} if summarized_article_ids else {}

        # Iterate over articles until we find one with content less than or equal to 1800 words
        for article in mongo.db.articles.find(query):
            word_count = len(article.get('content', '').split())
            if word_count <= 1800:
                article_to_summarize = article
                break
        if not article_to_summarize:
            return jsonify({"success": False, "message": "No new articles to summarize or all remaining articles are too long"}), 404


        # Serialize the whole article document into a JSON string using the custom encoder
        article_json_string = json.dumps(article_to_summarize, cls=JSONEncoder)

        # Get the summary for the article
        summarized_content = summarizer.generate_summary(article_json_string)

        # Parse the summarized content into a Python dict
        summarized_data = json.loads(summarized_content)
        print(summarized_data)
        # Remove quotes around bullet points
        summary_list = [item.strip('"') for item in summarized_data['Content']]

        # Construct the complete JSON object
        complete_json = {
            "_id": str(article_to_summarize['_id']),  # Convert ObjectId to string
            "category": article_to_summarize.get('category', ''),
            "title": summarized_data['Title'],
            "author": article_to_summarize.get('author', ''),
            "content": summary_list,
            "source": article_to_summarize.get('source', ''),
            "link": article_to_summarize.get('link', '')  # Assuming 'link' is an attribute in the article document
        }

        # Insert the summarized content, new title, and other relevant fields into summaries collection
        insert_summary_into_summaries(
            article_to_summarize['_id'],
            summarized_data['Title'],
            summary_list,
            article_to_summarize.get('category', ''),
            article_to_summarize.get('author', ''),
            article_to_summarize.get('source', ''),
            article_to_summarize.get('date', '')
        )

        return jsonify({"success": True, "message": "Article summarized successfully", "summary": complete_json}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



@summary_bp.route('/<category>', methods=['GET'])
def articles_by_category(category):
    try:
        valid_categories = ["politics", "nature", "technology", "science"]
        if category not in valid_categories:
            return jsonify({'error': 'Invalid category specified'}), 400

        articles = mongo.db.articles.find({'category': category})

        summarized_articles = list(articles)
        for article in summarized_articles:
            article['_id'] = str(article['_id'])

        return jsonify(summarized_articles), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    