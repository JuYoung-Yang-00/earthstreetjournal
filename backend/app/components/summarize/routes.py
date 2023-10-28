# app/components/summaries/routes.py
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)
from flask import Blueprint, jsonify
from config import Config
from app import mongo
from app.components.summarize.summarize import OpenAISummarizer
from bson import ObjectId, json_util 

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
 
    
@summary_bp.route('/summarize-article', methods=['GET'])
def summarize_article():
    try:
        summarizer = OpenAISummarizer(Config.OPENAI_API_KEY)

        # Get all the summarized article_ids from summaries collection
        summarized_article_ids = [summary['_id'] for summary in mongo.db.summaries.find({}, {"_id": 1})]

        # Fetch the first unsummarized article
        if summarized_article_ids:
            article = mongo.db.articles.find_one({'_id': {'$nin': summarized_article_ids}})
        else:
            article = mongo.db.articles.find_one({})

        # If there's no new article to summarize, return a message indicating so
        if not article:
            return jsonify({"success": False, "message": "No new articles to summarize"}), 404

        # Extract the relevant fields from the article
        article_content = article.get('content', '')
        article_title = article.get('title', '')
        category = article.get('category', '')
        author = article.get('author', '')
        source = article.get('source', '')
        date = article.get('date', '')

        # Combine the title and content and then get the summary
        combined_content = f"{article_title} \n \n {article_content}"
        new_title, summarized_content = summarizer.generate_summary(combined_content)

        # Insert the summarized content, new title, and other relevant fields into summaries collection
        insert_summary_into_summaries(article['_id'], new_title, summarized_content, category, author, source, date)

        return jsonify({"success": True, "message": "Article summarized successfully", "summary": summarized_content, "title": new_title}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
