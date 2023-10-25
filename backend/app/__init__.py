# app/__init__.py
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from config import Config
from flask_jwt_extended import JWTManager

mongo = PyMongo()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    
    mongo.init_app(app)

    try:
        _ = mongo.cx.server_info()  
        print("Connected to MongoDB!")
    except Exception as e:
        print("Could not connect to MongoDB:", e)
        
        
    jwt.init_app(app)

    from app.views.article_scrape.scrape_routes import scrape_bp
    from app.views.auth_routes.oauth import oauth_bp
    
    app.register_blueprint(oauth_bp, url_prefix='/oauth')
    app.register_blueprint(scrape_bp, url_prefix='/scrape')

    return app
