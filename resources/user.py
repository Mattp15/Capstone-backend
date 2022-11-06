import models
from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict

users = Blueprint('users', 'users')
user_things = Blueprint('user_things', 'user_things')
recipes = Blueprint('recipes', 'recipes')

@users.route('/', methods=["GET"])
def get_logged_in_user():
    user_dict = model_to_dict(current_user)
    user_dict.pop('password')
    return jsonify(
        data = user_dict,
        message = "Current User",
        status = 200
    ),200

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
        # else:
        #     return jsonify(
        #         data = {},
        #         message = "Username or Password doesn't not match.",
        #         message = 401
        #     ), 401
    except models.DoesNotExist:
        return jsonify(
            data={},
            message = "Username or Password do not match",
            status = 401
        ), 401

@users.route('/register', methods=["POST"])
def register():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    try:
        models.User.get(models.User.email == payload['email'])
        return jsonify(data={}, status={"code": 401, "message": "A user with that email already exists."})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        user = models.User.create(**payload)
        login_user(user)
        user_dict = model_to_dict(user)
        del user_dict['password']
        user_things = models.User_Things.create(**user_dict)

        return jsonify(
            data = user_dict,
            message = "Success",
            status = 200
        ), 200