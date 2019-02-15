import peewee
from tornado import web

from config import settings

db = peewee.SqliteDatabase(settings['db_name'])

from app.handlers.MainHandler import MainHandler
from app.handlers.RegHandler import RegHandler
from app.handlers.ProfileHandler import ProfileHandler
from app.handlers.LogOutHandler import LogOutHandler
from app.handlers.UsersJSONHandler import UsersJSONHandler
from app.handlers.RepositoriesHandler import RepositoriesHandler


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
