import peewee
from tornado import web

from config import settings

db = peewee.SqliteDatabase(settings['db_name'])

from app.MainHandler import MainHandler
from app.RegHandler import RegHandler
from app.ProfileHandler import ProfileHandler
from app.LogOutHandler import LogOutHandler
from app.UsersJSONHandler import UsersJSONHandler
from app.RepositoriesHandler import RepositoriesHandler


def make_app():
    return web.Application([
        (r'/', MainHandler),
        (r'/registration', RegHandler),
        (r'/profile/([^/]+)', ProfileHandler),
        (r'/logout', LogOutHandler),
        (r'/api/users', UsersJSONHandler),
        (r'/api/repositories/([^/]+)', RepositoriesHandler)
    ], **settings
    )


app = make_app()
