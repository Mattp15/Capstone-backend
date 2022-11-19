import models, random 
import recipes_objects
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict


recipes = Blueprint('recipes', 'recipes')


@recipes.route('/', methods=["GET"])
def get_all_recipes():
    try:
        all_recipes = models.Recipes.select()
        all_recipes_dict = [model_to_dict(recipe) for recipe in all_recipes]
        random.shuffle(all_recipes_dict)        
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
    for i in range(len(recipes_objects.recipes)):
        try:
            models.Recipes.get(models.Recipes.title == recipes_objects.recipes[i]['title'])
        except models.DoesNotExist:          
            recipe = models.Recipes.create(
                author_credit = recipes_objects.recipes[i]['author_credit'],
                calories = recipes_objects.recipes[i]['calories'],
                carbs = recipes_objects.recipes[i]['carbs'],
                category = recipes_objects.recipes[i]['category'],
                description = recipes_objects.recipes[i]['description'],
                fat = recipes_objects.recipes[i]['fat'],
                image = recipes_objects.recipes[i]['image'],
                ingredients = recipes_objects.recipes[i]['ingredients'],
                instructions = recipes_objects.recipes[i]['instructions'],
                protein = recipes_objects.recipes[i]['protein'],
                servings = recipes_objects.recipes[i]['servings'],
                shopping_list = recipes_objects.recipes[i]['shopping_list'],
                time = recipes_objects.recipes[i]['time'],
                title = recipes_objects.recipes[i]['title'],
            )
            recipe_dict = model_to_dict(recipe)
    return jsonify(
        data = recipe_dict,
        message = "Recipe succesfully added to database",
        status = 201
    ), 201