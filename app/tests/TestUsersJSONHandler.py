import base64

import requests
from tornado.testing import AsyncHTTPTestCase

import app


class TestUsersJSONHandler(AsyncHTTPTestCase):
    def get_app(self):
        return app.make_app()

    def test_get(self):
        url = 'http://127.0.0.1:8888/api/users'
        username = 'qwe'
        password = '123'
        basic_auth = base64.b64encode(str(username + ':' + password).encode('utf-8'))
        headers = {
            'Authorization': 'Basic ' + basic_auth.decode('utf-8'),
        }
        response = self.fetch(url, method='GET', headers=headers)
        self.assertNotEqual(response.code, 401, 'Ошибка авторизации')
        self.assertNotEqual(response.code, 500, 'Введены не верные данные')
