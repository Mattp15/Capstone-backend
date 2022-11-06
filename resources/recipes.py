import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

recipes = Blueprint('recipes', 'recipes')

#temporary for building
@recipes.route('/', methods=["GET"])
def get_all_recipes():
    all_recipes = models.Recipes.select()
    recipes_dict = model_to_dict(all_recipes)
    return jsonify(
        data = recipes_dict,
        message = "These are all the recipes in the database",
        status = 200
    ), 200
    
@recipes.route('/add', methods=["POST"])
def create_recipe():
    payload = request.get_json()
    try:
        models.Recipes.get(models.Recipes.title == payload['title'])
        return jsonify(
            data={},
            message = "That recipe already exists in the database",
            status = 409
        ), 409
    except models.DoesNotExist:
        recipe = models.Recipes.create(**payload)
        recipe_dict = model_to_dict(recipe)
        return jsonify(
            data = recipe_dict,
            message = "Recipe succesfully added to database",
            status = 201
        ), 201