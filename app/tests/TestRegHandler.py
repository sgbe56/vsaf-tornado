import requests
from tornado.testing import AsyncHTTPTestCase

import app


class TestRegHandler(AsyncHTTPTestCase):
    def get_app(self):
        return app.make_app()

    def test_get(self):
        url = 'http://127.0.0.1:8888/registration'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        url = 'http://127.0.0.1:8888/registration'
        data = {
            'username': 'qwe',
            'password': '123'
        }
        response = requests.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('Не все поля заполнены', response.text, 'Не все поля заполнены')
        self.assertIn('Пользователь с таким логином уже существует', response.text,
                      'Пользователь с таким логином уже существует')
