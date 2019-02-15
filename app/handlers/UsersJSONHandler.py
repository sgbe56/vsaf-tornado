import json

from tornado.web import RequestHandler

from app.AccessMixin import AccessMixin
from app.models import Users


class UsersJSONHandler(AccessMixin, RequestHandler):
    def prepare(self):
        super().prepare(valid_funcs=('GET',))

    def get(self):
        users = [user for user in Users.select(Users.username).dicts()]
        self.set_header('Content-type', 'application/json')
        return self.write(json.dumps(users, sort_keys=True, indent=4))
