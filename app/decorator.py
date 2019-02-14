import base64

from .AuthManager import AuthManager


def error_auth(handler):
    handler.set_header('WWW-Authenticate', 'Basic realm=vsaf')
    handler.set_status(401)
    return handler.write('Could not verify your access level for that URL.\n'
                         'You have to login with proper credentials')


def auth_required(cls, check_basic_auth=False):  # Проверка введенных данных, перед перенаправлением в профиль
    if not cls.get_secure_cookie('username'):
        if check_basic_auth:
            auth = cls.request.headers.get('Authorization', None)

            if auth is None:
                return error_auth(cls)

            username, password = tuple(base64.b64decode(auth[6:].encode('utf-8')).decode('utf-8').split(':'))

            if AuthManager.check_user(username, password):
                cls.set_secure_cookie('username', username)
                return cls
            else:
                error_auth(cls)
        return cls.redirect('/')
    return cls


class AccessMixin:
    def prepare(self, valid_funcs=('GET', 'POST', 'PATCH', 'PUT', 'DELETE', 'HEAD', 'OPTIONS')):
        super().prepare()
        if self.request.method in valid_funcs:
            auth_required(self, True)
