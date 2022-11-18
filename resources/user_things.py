import models, random
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

user_things = Blueprint('user_things', 'user_things')






#! REALLY TRY TO GET THAT DELTE BY FOREIGN KEY ID WORKING
#TODO Make a route to remove dislike and favorite by id, should just be user_thing id not recipe_id.id


#Get's all of current users's User_Things
@user_things.route('/', methods=["GET"])
def get_current_user_recipes():
        try:
            user_things = models.User_Thing.select().where(models.User_Thing.user_id == current_user)
            things_dict = [model_to_dict(thing) for thing in user_things]
            return jsonify(
                data = things_dict,
                message = "Pulled things from databas",
                status = 200
            ), 200
        except models.DoesNotExist:
            return jsonify(
                data = {},
                message = "There is no such thing",
                status = 404
            ), 404

#Creates a User_Thing for current user/Deletes
@user_things.route('/<id>', methods=["POST", "DELETE"])
def create_user_thing(id):
    if request.method == "POST":
        payload = request.get_json()
        print(payload)
        try:
            recipe = models.Recipes.get_by_id(id)
            recipe_dict = model_to_dict(recipe)
            try:
                check = models.User_Thing.select()
                check_dict = [model_to_dict(thing) for thing in check]
                for i in range(len(check_dict)):
                    
                    if (int(id) == check_dict[i]['recipe_id']['id'] and current_user.id == check_dict[i]['user_id']):
                        return jsonify(
                            message = "Already Exists",
                            status = 409
                        ), 409

                else:      

                    new_thing = models.User_Thing.create(
                        #**payload,this doesnt work
                        dislike = payload['dislike'],
                        favorite = payload['favorite'],
                        recipe_id = recipe_dict['id'],
                        user_id = current_user.id
                    )
                    new_thing_dict = model_to_dict(new_thing)
                    return jsonify(
                        data = new_thing_dict,
                        message = "Successfully added recipe to User_things",
                        status = 200
                    ), 200
            except:
                pass
        except:
            return jsonify(
                data={},
                message = "Failled to add to User_Things",
                status = 409
            ), 409
    elif request.method == "DELETE":
        #deletes the User_Thing table by user_id and User_Thing.id == passed param called id
        try:          

            deleted = models.User_Thing.delete().where(current_user == models.User_Thing.user_id and models.User_Thing.id == id)
            deleted.execute()
            return jsonify(
                message = "Successfully deleted", 
                status = 204
            ), 204
        except models.DoesNotExist:
            return jsonify(

            ), 404

            