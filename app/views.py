import json

import tornado.web
from tornado import httpclient

from .AuthManager import AuthManager
from .decorator import AccessMixin
from .models import Users


class ApplicationHandler(tornado.web.RequestHandler):
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


class MainHandler(ApplicationHandler):
    def get(self):
        return self.render('templates/index.html', users_list=self.users_list, error=0, title='Log In')

    def post(self):
        if self.get_argument('username') and self.get_argument('password'):
            username = self.get_argument('username')
            valid_data = AuthManager.check_user(username, self.get_argument('password'))
            if valid_data:
                self.set_secure_cookie('username', username)
                return self.redirect('/profile/' + username)
            else:
                return self.render('templates/index.html', users_list=self.users_list, error=2, title='Log In')
        else:
            return self.render('templates/index.html', users_list=self.users_list, error=1, title='Log In')


class RegHandler(ApplicationHandler):
    def get(self):
        return self.render('templates/registration.html', error=0, title='Sign Up')

    def post(self):
        if self.get_argument('username') and self.get_argument('password'):
            username = self.get_argument('username')
            login_exist = AuthManager.register_user(username, self.get_argument('password'))
            if not login_exist:
                self.set_secure_cookie('username', username)
                return self.redirect('/profile/' + username)
            else:
                return self.render('templates/registration.html', error=2, title='Sign Up')
        else:
            return self.render('templates/registration.html', error=1, title='Sign Up')


class LogOutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_all_cookies()
        return self.redirect('/')


class ProfileHandler(ApplicationHandler):
    def prepare(self):
        pass

    def get(self, username):
        guest = False
        if self.current_user:
            if not self.current_user == username:
                try:
                    Users.get(Users.username == username).username
                    guest = True
                except Users.DoesNotExist:
                    return self.redirect('/profile/' + self.get_current_user())

            return self.render('templates/profile.html', username=username, guest=guest,
                               title=username + f'\'s profile')
        return self.redirect('/')


class UsersJSONHandler(AccessMixin, tornado.web.RequestHandler):
    def prepare(self):
        super().prepare(valid_funcs=('GET',))

    def get(self):
        users = [user for user in Users.select(Users.username).dicts()]
        self.set_header('Content-type', 'application/json')
        return self.write(json.dumps(users, sort_keys=True, indent=4))


class RepositoriesHandler(tornado.web.RequestHandler):
    async def get(self, login):
        url = f'https://api.github.com/users/{login}/repos'
        http_client = httpclient.AsyncHTTPClient()
        try:
            response = await http_client.fetch(url, headers={'User-Agent': login})
        except httpclient.HTTPClientError as e:
            return self.write(f'Error: {e}')
        else:
            repositories = json.loads(response.body)
            return self.write(json.dumps([rep['name'] for rep in repositories], sort_keys=True))
