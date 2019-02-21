import requests
from tornado.testing import AsyncHTTPTestCase

import app


class TestMainHandler(AsyncHTTPTestCase):
    def get_app(self):
        return app.make_app()

    def test_get(self):
        url = 'http://127.0.0.1:8888/'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        url = 'http://127.0.0.1:8888/'
        username = 'qwe'
        password = '123'
        data = {
            'username': username,
            'password': password
        }
        response = requests.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Не все поля заполнены', response.text, 'Не все поля заполнены')
        self.assertNotIn('Введены неверные логин или пароль', response.text, 'Введены неверные логин или пароль')
