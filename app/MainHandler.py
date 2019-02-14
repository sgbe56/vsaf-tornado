from .ApplicationHandler import ApplicationHandler
from .AuthManager import AuthManager


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
