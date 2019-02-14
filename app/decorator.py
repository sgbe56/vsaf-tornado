import base64
import inspect
from functools import wraps

from .AuthManager import AuthManager


def error_auth(handler):
    handler.set_header('WWW-Authenticate', 'Basic realm=vsaf')
    handler.set_status(401)
    return handler.write('Could not verify your access level for that URL.\n'
                         'You have to login with proper credentials')


def auth_required(handler, check_basic_auth=True):  # Проверка введенных данных, перед перенаправлением в профиль
    @wraps(handler)
    def wrapper(*args, **kwargs):
        if not args[0].get_secure_cookie('username'):
            if check_basic_auth:
                auth = args[0].request.headers.get('Authorization', None)

                if auth is None:
                    return error_auth(args[0])

                username, password = tuple(base64.b64decode(auth[6:].encode('utf-8')).decode('utf-8').split(':'))

                if AuthManager.check_user(username, password):
                    args[0].set_secure_cookie('username', username)
                    return handler(*args, **kwargs)
                else:
                    error_auth(args[0])
            return args[0].redirect('/')
        return handler(*args, **kwargs)

    return wrapper


class Decorator:
    def __init__(self, list_of_valid_funcs=['get', 'post', 'patch', 'put', 'delete', 'head', 'options']):
        self.list_of_valid_funcs = list_of_valid_funcs

    def __call__(self, *args, **kwargs):
        for name, func in inspect.getmembers(args[0], inspect.isfunction):
            if name in self.list_of_valid_funcs:
                setattr(args[0], name, auth_required(func))
