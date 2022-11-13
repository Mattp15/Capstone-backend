import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict


recipes = Blueprint('recipes', 'recipes')


@recipes.route('/', methods=["GET"])
def get_all_recipes():
    try:
        all_recipes = models.Recipes.select()
        all_recipes_dict = [model_to_dict(recipe) for recipe in all_recipes]
        return jsonify(
            data = all_recipes_dict,
            message = "Here are all the recipes in the database",
            status = 200
        ), 200
    except:
        return jsonify(
            data = {},
            message = "FAILED TO GET ALL RECIPES",
            status = 404
        ), 404
        pass

#gets recipe at index of id
@recipes.route('/<id>', methods=["GET"])
def get_recipe(id):
    try:
        recipe = models.Recipes.get_by_id(id)
        recipe_dict = model_to_dict(recipe)
        return jsonify(
            data = recipe_dict,
            message = "This is the requested recipe",
            status = 200
        ), 200
    except models.DoesNotExist:
        return jsonify(
            data = {},
            message = "This recipe ID does not exist",
            status = 404
        ), 404

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