from peewee import *
import datetime
from flask_login import UserMixin

DATABASE = SqliteDatabase('thigs.SQLite')


class User(UserMixin, Model):
    #add admin for adding recipies//changing user data on the web interface
    created = DateTimeField(default=datetime.datetime.now)
    email = CharField(unique=True)
    password = CharField()
    class Meta:
        database = DATABASE


class Recipes(Model):
    author_credit = CharField()
    image = CharField()
    calories = IntegerField()
    carbohydrate = IntegerField()
    fat = IntegerField()
    ingredients = CharField()#Change to array of objects
    instructions = CharField()#should be array of lists
    title = CharField(unique=True)
    protein = IntegerField()
    shopping_list = CharField()#change to array of objects

    class Meta:
        database = DATABASE

class User_Thing(Model):
    dislike = BooleanField(default=False)
    favorite = BooleanField(default=False)
    recipe_id = ForeignKeyField(Recipes, backref='recipes')
    recipe_created = DateTimeField(default=datetime.datetime.now)
    user_id = IntegerField()
    
    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, User_Thing, Recipes], safe=True)
    print("Connected to the DB and created tables if they didn't exist")
    DATABASE.close()