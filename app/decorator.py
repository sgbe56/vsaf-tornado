import base64
import inspect
from functools import wraps

from .AuthManager import AuthManager


def error_auth(handler):
    handler.set_header('WWW-Authenticate', 'Basic realm=vsaf')
    handler.set_status(401)
    return handler.write('Could not verify your access level for that URL.\n'
                         'You have to login with proper credentials')


def auth_required(cls, handler, check_basic_auth=True):  # Проверка введенных данных, перед перенаправлением в профиль
    @wraps(handler)
    def wrapper(*args, **kwargs):
        if not cls.get_secure_cookie('username'):
            if check_basic_auth:
                auth = cls.request.headers.get('Authorization', None)

                if auth is None:
                    return error_auth(cls)

                username, password = tuple(base64.b64decode(auth[6:].encode('utf-8')).decode('utf-8').split(':'))

                if AuthManager.check_user(username, password):
                    cls.set_secure_cookie('username', username)
                    return handler(*args, **kwargs)
                else:
                    error_auth(cls)
            return cls.redirect('/')
        return handler(*args, **kwargs)

    return wrapper


class AccessMixin:
    def prepare(self, cls, valid_funcs=('get', 'post', 'patch', 'put', 'delete', 'head', 'options')):
        super().prepare()

        all_funcs = dict(inspect.getmembers(cls, inspect.ismethod(object)))
        existing_funcs = [(valid_func, all_funcs[valid_func]) for valid_func in valid_funcs
                          if all_funcs[valid_func] is not None]

        for name, func in existing_funcs:
            if name in valid_funcs:
                setattr(cls, name, auth_required(cls, func))
