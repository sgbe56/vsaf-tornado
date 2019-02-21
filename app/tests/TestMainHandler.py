import urllib

from tornado.testing import AsyncHTTPTestCase

import app


class TestMainHandler(AsyncHTTPTestCase):
    def get_app(self):
        return app.make_app()

    def test_get(self):
        url = 'http://127.0.0.1:8888/'
        response = self.fetch(url, method='GET')
        self.assertEqual(response.code, 200)

    def test_post(self):
        url = 'http://127.0.0.1:8888/'
        username = 'qwe'
        password = '123'
        body = urllib.parse.urlencode({
            'username': username,
            'password': password
        })
        response = self.fetch(url, method='POST', body=body)
        self.assertEqual(response.code, 200)
        self.assertNotIn('Не все поля заполнены', response.body.decode('utf-8'), 'Не все поля заполнены')
        self.assertNotIn('Введены неверные логин или пароль', response.body.decode('utf-8'),
                         'Введены неверные логин или пароль')
