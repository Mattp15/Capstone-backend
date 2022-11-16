import models, re, random
from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from playhouse.shortcuts import model_to_dict



users = Blueprint('users', 'users')


#Get's current user
@users.route('/account', methods=["GET"])
@login_required
def get_logged_in_user():
    try:
        user_dict = model_to_dict(current_user)
        print(user_dict)
        user_dict.pop('password')
        return jsonify(
            data = user_dict,
            message = "Current User",
            status = 200
        ),200
    except:
        return jsonify(
            data ={},
            message = "No user logged in",
            status = 404
        ), 404

#User Login
@users.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    try:
        user = models.User.get(models.User.email == payload['email'].lower())
        user_dict = model_to_dict(user)
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)
            return jsonify(
                data = user_dict,
                message = "Logged in successfully",
                status = 200
            ), 200
    except models.DoesNotExist:
        return jsonify(
            data={},
            message = "Username or Password do not match",
            status = 404
        ), 404

#Log out current_user
@users.route('/logout', methods=["GET"])
def logout_user():
    # user = model_to_dict(current_user)
    
    try:
        logout_user()
        user_dict = model_to_dict(current_user)
        return jsonify(
            data = user_dict,
            message = f'User has been logged out',
            status = 200
        ), 200
    except:
        return jsonify(
            message = "no user is logged in",
            status = 404
        ), 404

#Register new user + logs in user as current_user
@users.route('/register', methods=["POST"])
def register():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    if is_valid(payload['email']):
        try:
            models.User.get(models.User.email == payload['email'])
            return jsonify(
                data = {},
                message = "A user with that email already exists.",
                status = 401,
            ), 401
        except models.DoesNotExist:
            payload['password'] = generate_password_hash(payload['password'])
            user = models.User.create(**payload)
            login_user(user)
            user_dict = model_to_dict(user)
            del user_dict['password']
            return jsonify(
                data = user_dict,
                message = "Success",
                status = 200
            ), 200
    else:
        return jsonify(
            data={},
            message = "Email does not meet criteria",
            status = 400
        ), 400

def is_valid(email):
    email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(email_regex, email):
        return True
    else:
        return False