import models, re, random
from flask import request, jsonify, Blueprint, session
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from playhouse.shortcuts import model_to_dict



users = Blueprint('users', 'users')
user_list = Blueprint('user_list', 'user_list')

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

@users.route('/list', methods=["GET", "POST", "DELETE"])
def handle_users_list():
    if request.method == "DELETE":
        payload = request.get_json()
        try:
            print(current_user, payload['id'])
            # deleted = models.User_List.delete().where(models.User_List.recipe_id.id == payload['id'] and models.User_List.user_id == current_user)
            test = models.User_List.get_by_id(payload['id'])
            deleted = models.User_List.delete().where(models.User_List.id == payload['id'])
            deleted.execute()
            return jsonify(
                message = "Item has been deleted from users active list",
                status = 205,
            ), 205

        except models.DoesNotExist:
            return jsonify(
                message = "No such item to delete",
                status = 404
            ), 404

    if request.method == "GET":
        print(current_user, 'current')
        users_list = models.User_List.select().where(models.User_List.user_id == current_user)
        users_list_dict = [model_to_dict(u_list) for u_list in users_list]
        print(users_list_dict, 'users_list_dict')
        return jsonify(
            data = users_list_dict,
            message = "Found",
            status = 200
        ), 200


    if request.method == "POST":
        payload = request.get_json()
        try:
            check_recipe_exists = models.Recipes.get_by_id(payload['id'])
            exists = models.User_List.select().where(models.User_List.user_id == current_user and models.User_List.recipe_id)
            exists_dict = [model_to_dict(item) for item in exists]
            for i in range(len(exists_dict)):
                if exists_dict[i]['recipe_id']['id'] == payload['id']:
                    return jsonify(
                    message = "recipe is already in your list"
                    )
                
            print(len(exists_dict))
            recipe = models.Recipes.get_by_id(payload['id'])
            create = models.User_List.create(
                user_id = current_user,
                recipe_id = payload['id']
            )
            return jsonify(
                message = "Added to list",
                status = 200
            ),200
        except models.DoesNotExist:
            return jsonify(
                message = "no such recipe to add",
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
            session["name"] = payload["email"]
            print(session['name'])
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