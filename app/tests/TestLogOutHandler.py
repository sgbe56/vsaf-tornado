import requests
from tornado.testing import AsyncHTTPTestCase
from tornado.web import create_signed_value

import app


class TestLogOutHandler(AsyncHTTPTestCase):
    def get_app(self):
        return app.make_app()

    def test_get(self):
        url = 'http://127.0.0.1:8888/logout'
        username = 'qwe'
        secure_cookie = create_signed_value(app.settings["cookie_secret"], 'username', username)
        headers = {
            'Cookie': '='.join(('username', secure_cookie.decode('utf-8')))
        }
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
