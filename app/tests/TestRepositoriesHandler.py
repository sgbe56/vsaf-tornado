from tornado.testing import AsyncHTTPTestCase

import app


class TestRepositoriesHandler(AsyncHTTPTestCase):
    def get_app(self):
        return app.make_app()

    def test_get(self):
        github_username = 'github'
        url = 'http://127.0.0.1:8888/api/repos/' + github_username
        self.http_client.fetch(url, self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200, 'Ошибка')
