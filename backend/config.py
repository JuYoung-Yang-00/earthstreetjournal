import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_USER = os.getenv('MONGO_USER')
    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
    MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@cluster0.dcq21ni.mongodb.net/earthstreetjournal?retryWrites=true&w=majority"
    SECRET_KEY = os.getenv('SECRET_KEY')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

