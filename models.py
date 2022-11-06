from peewee import *
import datetime
from flask_login import UserMixin

DATABASE = SqliteDatabase('thigs.py')

class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField(unique=True)
    created = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = DATABASE

class User_Things(Model):
    dislik = BooleanField(default=False)
    favorite = BooleanField(default=False)
    recipe = CharField()
    recipe_created = DateTimeField(default=datetime.datetime.now)
    user_id = ForeignKeyField(User, backref='id')
    

    class Meta:
        database = DATABASE

class Recipes(Model):
    name = CharField()
    nutrition = CharField()
    ingredients = CharField()
    instructions = CharField()
    author_credit = CharField()
    shopping_list = CharField()

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, User_Things, Recipes], safe=True)
    print("Connected to the DB and created tables if they didn't exist")
    DATABASE.close()