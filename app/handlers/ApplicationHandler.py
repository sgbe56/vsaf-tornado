from tornado.web import RequestHandler

from app.models import Users


class ApplicationHandler(RequestHandler):
    def initialize(self):
        self.current_user = self.get_current_user()
        self.users_list = self.get_all_users()

    def get_current_user(self):
        if self.get_secure_cookie('username') is not None:
            return self.get_secure_cookie('username').decode('utf-8')

    def get_all_users(self):
        return [user[0] for user in Users.select(Users.username).tuples()]

    def prepare(self):
        if self.current_user:
            return self.redirect('/profile/' + self.current_user)
