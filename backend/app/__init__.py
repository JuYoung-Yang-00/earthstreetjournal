from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from config import Config
from flask_jwt_extended import JWTManager
from bson import ObjectId
import json 

mongo = PyMongo()
jwt = JWTManager()

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Use the custom JSONEncoder
    app.json_encoder = CustomJSONEncoder
    
    CORS(app)
    mongo.init_app(app)

    try:
        _ = mongo.cx.server_info()  
        print("Connected to MongoDB!")
    except Exception as e:
        print("Could not connect to MongoDB:", e)
        
    jwt.init_app(app)

    from app.components.article_scrape.scrape_routes import scrape_bp
    from app.components.auth_routes.oauth import oauth_bp
    from app.components.summarize.routes import summary_bp
    from app.components.summarized.routes import summarized_bp
    
    app.register_blueprint(oauth_bp, url_prefix='/oauth')
    app.register_blueprint(scrape_bp, url_prefix='/scrape')
    app.register_blueprint(summary_bp, url_prefix='/summarize')
    app.register_blueprint(summarized_bp, url_prefix='/summarized')

    return app
