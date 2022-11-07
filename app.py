from flask import Flask, jsonify
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


app.secret_key = os.environ.get("APP_SECRET")
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        pass

app.register_blueprint(users, url_prefix='/user')
app.register_blueprint(recipes, url_prefix='/recipes')
app.register_blueprint(user_things, url_prefix='/user/index')



if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
