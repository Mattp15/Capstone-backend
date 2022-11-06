from peewee import *
import datetime
from flask_login import UserMixin

DATABASE = SqliteDatabase('thigs.py')

class User(UserMixin, Model):
    created = DateTimeField(default=datetime.datetime.now)
    email = CharField(unique=True, null=True)
    password = CharField(null=True)
    class Meta:
        database = DATABASE

class User_Things(Model):
    dislik = BooleanField(default=False)
    favorite = BooleanField(default=False)
    recipe_id = IntegerField(null=True)
    recipe_created = DateTimeField(default=datetime.datetime.now)
    user_id = ForeignKeyField(User, null=True, backref='id')
    

    class Meta:
        database = DATABASE

class Recipes(Model):
    author_credit = CharField(null=True)
    ingredients = CharField(null=True)
    instructions = CharField(null=True)
    title = CharField(null=True)
    protein = CharField(null=True)
    shopping_list = CharField(null=True)
    total_fat = CharField(null=True)
    total_carbohydrate = CharField(null=True)

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, User_Things, Recipes], safe=True)
    print("Connected to the DB and created tables if they didn't exist")
    DATABASE.close()