import base64
import re
from .AuthManager import AuthManager


def base64_parser(self, auth):
    if re.match(r'Basic\s', auth):
        auth = re.sub(r'Basic\s', '', auth)
        if not re.findall(f'\s+', auth):
            auth = base64.b64decode(auth.encode('utf-8')).decode('utf-8')
            return tuple(re.split(r':', auth))
        else:
            return error_auth(self)
    return error_auth(self)


def error_auth(self):
    self.set_header('WWW-Authenticate', 'Basic realm=vsaf')
    self.set_status(401)
    return self.write('Could not verify your access level for that URL.\n'
                         'You have to login with proper credentials')


def auth_required(self, check_basic_auth=False):
    if not self.get_secure_cookie('username'):
        if check_basic_auth:
            auth = self.request.headers.get('Authorization', None)

            if auth is None:
                return error_auth(self)

            username, password = base64_parser(self, auth)

            if AuthManager.check_user(username, password):
                self.set_secure_cookie('username', username)
                return self
            else:
                error_auth(self)
        return self.redirect('/')
    return self


class AccessMixin:
    def prepare(self, valid_funcs=('get', 'post', 'patch', 'put', 'delete', 'head', 'options')):
        super().prepare()
        if self.request.method.lower() in valid_funcs:
            auth_required(self, True)