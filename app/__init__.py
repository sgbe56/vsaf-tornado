import peewee
import tornado

from config import settings

db = peewee.SqliteDatabase(settings['db_name'])

from .views import MainHandler, RegHandler, ProfileHandler, LogOutHandler, UsersJSONHandler, RepositoriesHandler


def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/registration', RegHandler),
        (r'/profile/([^/]+)', ProfileHandler),
        (r'/logout', LogOutHandler),
        (r'/api/users', UsersJSONHandler),
        (r'/api/repositories/([^/]+)', RepositoriesHandler)
    ], **settings
    )


app = make_app()
