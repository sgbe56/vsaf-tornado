import json

import tornado.web
from tornado.httpclient import HTTPClient, AsyncHTTPClient

from .AuthManager import AuthManager
from .decorator import access
from .models import Users


class MainHandler(tornado.web.RequestHandler):
    def prepare(self):
        global session_user
        session_user = self.get_secure_cookie('username')

        if session_user:
            return self.redirect('/profile/' + session_user.decode('utf-8'))

        global users_list
        users_list = [user[0] for user in Users.select(Users.username).tuples()]

    def get(self):
        return self.render('templates/index.html', users_list=users_list, error=0, title='Log In')

    def post(self):
        users_list = [user[0] for user in Users.select(Users.username).tuples()]

        if self.get_argument('username') and self.get_argument('password'):
            username = self.get_argument('username')
            valid_data = AuthManager.check_user(username, self.get_argument('password'))
            if valid_data:
                self.set_secure_cookie('username', username)
                return self.redirect('/profile/' + username)
            else:
                return self.render('templates/index.html', users_list=users_list, error=2, title='Log In')
        else:
            return self.render('templates/index.html', users_list=users_list, error=1, title='Log In')


class RegHandler(tornado.web.RequestHandler):
    def prepare(self):
        global session_user
        session_user = self.get_secure_cookie('username')

        if session_user:
            return self.redirect('/profile/' + session_user.decode('utf-8'))

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


class ProfileHandler(tornado.web.RequestHandler):
    def get(self):
        guest = False
        username = self.request.path.split('/')[2]
        if self.get_secure_cookie('username'):
            if not self.get_secure_cookie('username').decode('utf-8') == username:
                try:
                    Users.get(Users.username == username).username
                    guest = True
                except Users.DoesNotExist:
                    return self.redirect('/profile/' + self.get_secure_cookie('username').decode('utf-8'))

            return self.render('templates/profile.html', username=username, guest=guest,
                               title=username + f'\'s profile')
        return self.redirect('/')


class UsersJSONHandler(tornado.web.RequestHandler):
    @access(check_basic_auth=True)
    def get(self):
        users = [user for user in Users.select(Users.username).dicts()]
        self.set_header('Content-type', 'application/json')
        return self.write(json.dumps(users, sort_keys=True, indent=4))


class RepositoriesHandler(tornado.web.RequestHandler):
    async def get(self):
        login = self.request.path.split('/')[3]
        url = f'https://api.github.com/users/{login}/repos'
        http_client = AsyncHTTPClient()
        try:
            response = await http_client.fetch(url, headers={'User-Agent': 'sgbe56'})
        except Exception as e:
            return self.write(f'Error: {e}')
        else:
            repositories = json.loads(response.body)
            return self.write(json.dumps([rep['name'] for rep in repositories], sort_keys=True))
