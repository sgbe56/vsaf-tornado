import requests
from tornado.testing import AsyncHTTPTestCase
from tornado.web import create_signed_value

import app


class TestProfileHandler(AsyncHTTPTestCase):
    def get_app(self):
        return app.make_app()

    def test_get(self):
        username = 'qwe'
        username_in_url = 'qwe'
        url = 'http://127.0.0.1:8888/profile/' + username_in_url
        secure_cookie = create_signed_value(app.settings["cookie_secret"], 'username', username)
        headers = {
            'Cookie': '='.join(('username', secure_cookie.decode('utf-8')))
        }
        response = self.fetch(url, method='GET', headers=headers)
        self.assertEqual(response.code, 200)
        self.assertIn('Привет, ' + username_in_url, response.body.decode('utf-8'))
        self.assertEqual(username, username_in_url, 'Посещение не своего профиля')
