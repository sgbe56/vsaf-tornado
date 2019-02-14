from .ApplicationHandler import ApplicationHandler
from .AuthManager import AuthManager


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
