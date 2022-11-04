import models
from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict

users = Blueprint('users', 'users')

@users.route('/', methods=["GET"])
def show_users():
    return jsonify(
        data = 'blah blah',
        message = "Test successful",
        status = 200
    ), 200
