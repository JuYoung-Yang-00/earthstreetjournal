from flask import Blueprint, redirect, url_for, request, session, jsonify
from flask_jwt_extended import create_access_token
import secrets
from urllib.parse import urlencode
import requests
from config import Config
from app.models.user import User
from pymongo import MongoClient

oauth_bp = Blueprint('oauth', __name__)

OAUTH2_PROVIDERS = {
    'google': {
        'client_id': Config.GOOGLE_CLIENT_ID,
        'client_secret': Config.GOOGLE_CLIENT_SECRET,
        'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
        'token_url': 'https://accounts.google.com/o/oauth2/token',
        'userinfo': {
            'url': 'https://www.googleapis.com/oauth2/v3/userinfo',
            'email': lambda json: json['email'],
        },
        'scopes': ['https://www.googleapis.com/auth/userinfo.email'],
    }
}

@oauth_bp.route('/')
def index():
    return jsonify({"message": "API is working!"})

@oauth_bp.route('/logout')
def logout():
    return jsonify({"message": "Logged out!"})

@oauth_bp.route('/authorize/<provider>')
def oauth2_authorize(provider):
    provider_data = OAUTH2_PROVIDERS.get(provider)
    if provider_data is None:
        return jsonify({"error": "Invalid provider"}), 404
    session['oauth2_state'] = secrets.token_urlsafe(16)
    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('oauth.oauth2_callback', provider=provider, _external=True),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': session['oauth2_state'],
    })
    return redirect(provider_data['authorize_url'] + '?' + qs)

@oauth_bp.route('/callback/<provider>')
def oauth2_callback(provider):
    provider_data = OAUTH2_PROVIDERS.get(provider)
    
    if provider_data is None:
        return jsonify({"error": "Invalid provider"}), 404

    if 'error' in request.args:
        return jsonify({"error": request.args['error']})

    if request.args.get('state') != session.get('oauth2_state'):
        return jsonify({"error": "Invalid OAuth state"}), 401

    if 'code' not in request.args:
        return jsonify({"error": "No authorization code provided"}), 401
    
    response = requests.post(provider_data['token_url'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('oauth.oauth2_callback', provider=provider, _external=True),
    }, headers={'Accept': 'application/json'})

    if response.status_code != 200:
        return jsonify({"error": "Failed to retrieve OAuth token"}), 401

    oauth2_token = response.json().get('access_token')
    if not oauth2_token:
        return jsonify({"error": "Invalid OAuth token"}), 401

    response = requests.get(provider_data['userinfo']['url'], headers={
        'Authorization': 'Bearer ' + oauth2_token,
        'Accept': 'application/json',
    })
    if response.status_code != 200:
        return jsonify({"error": "Failed to retrieve user information"}), 401
    
    email = provider_data['userinfo']['email'](response.json())

    with MongoClient(Config.MONGO_URI) as client:
        db = client['earthstreetjournal']
        user = db.users.find_one({"email": email})

        if user is None:
            user_data = {
                "email": email,
                "username": email.split('@')[0]
            }
            db.users.insert_one(user_data)
            user = User(user_data)
        else:
            user = User(user)

    access_token = create_access_token(identity=user.email)
    return jsonify(access_token=access_token)
