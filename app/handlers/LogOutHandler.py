from tornado.web import RequestHandler


class LogOutHandler(RequestHandler):
    def get(self):
        self.clear_all_cookies()
        return self.redirect('/')
