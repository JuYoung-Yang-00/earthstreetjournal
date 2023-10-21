# app/__init__.py
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from config import Config


mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    CORS(app)
    
    mongo.init_app(app)


    from app.views.routes import route_bp
    app.register_blueprint(route_bp)

    return app
