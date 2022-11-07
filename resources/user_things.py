import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

user_things = Blueprint('user_things', 'user_things')

@user_things.route('/<id>', methods=["POST", "GET", "DELETE", "PUT"])
def create_user_thing(id):
    if request.method == "POST":
        try:
            recipe = models.Recipes.get_by_id(id)
            recipe_dict = model_to_dict(recipe)
            user_dict = model_to_dict(current_user)
            new_thing = models.User_Thing.create(
                recipe_id = recipe_dict['id'],
                user_id = user_dict['id']
            )
            new_thing_dict = model_to_dict(new_thing)
            print(new_thing_dict)
            return jsonify(
                data = new_thing_dict,
                message = "Successfully added recipe to User_things",
                status = 200
            ), 200
        except:
            return jsonify(
                data={},
                message = "Failled to add to User_Things",
                status = 409
            ), 409
    if request.method == "GET":
        try:
            user = current_user
            user_dict = model_to_dict(user)
            user_id = user_dict['id']
            print(user_id)
            thing = models.User_Thing.get_by_id(id)
            thing_dict = model_to_dict(thing)
            return jsonify(
                data = thing_dict,
                message = "Pulled thing from databas",
                status = 200
            ), 200
        except models.DoesNotExist:
            return jsonify(
                data = {},
                message = "There is no such thing",
                status = 404
            ), 404