import json

from tornado import httpclient
from tornado.web import RequestHandler


class RepositoriesHandler(RequestHandler):
    async def get(self, login):
        url = f'https://api.github.com/users/{login}/repos'
        http_client = httpclient.AsyncHTTPClient()
        try:
            response = await http_client.fetch(url, headers={'User-Agent': login})
        except httpclient.HTTPClientError as e:
            self.set_status(404)
            return self.write(f'Error: {e}')
        else:
            repositories = json.loads(response.body)
            return self.write(json.dumps([rep['name'] for rep in repositories], sort_keys=True))
