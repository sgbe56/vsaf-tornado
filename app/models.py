import peewee

from app import db


class Users(peewee.Model):
    id = peewee.PrimaryKeyField(null=False)
    username = peewee.TextField(unique=True, null=False)
    password = peewee.TextField(null=False)

    class Meta:
        database = db
        db_table = 'users'
