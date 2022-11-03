from flask import Flask, jsonify
import models
from flask_cors import CORS
from flask_login import LoginManager
import os
from dotenv import load_dotenv


load_dotenv()

DEBUG = True
PORT = os.environ.get("PORT")

app = Flask(__name__)


app.secret_key = os.environ.get("APP_SECRET")
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return ##
    except models.DoesNotExist:
        pass