import tornado

from app import app

if __name__ == "__main__":
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
