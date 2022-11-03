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
    email = ForeignKeyField(User, backref='user_things')
    