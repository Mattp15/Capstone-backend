from peewee import *
import datetime
from flask_login import UserMixin

DATABASE = SqliteDatabase('thigs.SQLite')

class User(UserMixin, Model):
    created = DateTimeField(default=datetime.datetime.now)
    email = CharField(unique=True)
    password = CharField()
    class Meta:
        database = DATABASE


class Recipes(Model):
    author_credit = CharField()
    ingredients = CharField()
    instructions = CharField()
    title = CharField(unique=True)
    protein = CharField()
    shopping_list = CharField()
    total_fat = CharField()
    total_carbohydrate = CharField()

    class Meta:
        database = DATABASE

class User_Thing(Model):
    dislike = BooleanField(default=False)
    favorite = BooleanField(default=False)
    recipe_id = ForeignKeyField(Recipes, backref='recipes')
    recipe_created = DateTimeField(default=datetime.datetime.now)
    # user_id = ForeignKeyField(User, backref='user')
    user_id = IntegerField()
    

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, User_Thing, Recipes], safe=True)
    print("Connected to the DB and created tables if they didn't exist")
    DATABASE.close()