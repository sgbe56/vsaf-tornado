from .ApplicationHandler import ApplicationHandler
from .models import Users


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
