from flask import Flask, jsonify, request, session, after_this_request
from flask_session import Session
import models
from flask_cors import CORS
from flask_login import LoginManager

import os
from dotenv import load_dotenv

from resources.recipes import recipes
from resources.user import users
from resources.user_things import user_things

load_dotenv()

DEBUG = True
PORT = os.environ.get("PORT")

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
Session(app)

app.secret_key = os.environ.get("APP_SECRET")
login_manager = LoginManager()
login_manager.init_app(app)
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='None',
)
sess = Session()
sess.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        pass




CORS(users, origins=['http://localhost:3000'], supports_credentials=True)
CORS(recipes, origins=['http://localhost:3000'], supports_credentials=True)
CORS(user_things, origins=['http://localhost:3000'], supports_credentials=True)


app.register_blueprint(users, url_prefix='/user')
app.register_blueprint(recipes, url_prefix='/recipes')
app.register_blueprint(user_things, url_prefix='/things')

@app.before_request
def before_request():
    """Connect to the db before each request"""
    print('you should see this before each request')
    models.DATABASE.connect()
    
    @after_this_request
    def after_request(response):
        print('you should see this after each request')
        models.DATABASE.close()
        return response

if os.environ.get('FLASK_ENV') != 'development':
    print('/non heroku!')
    models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
