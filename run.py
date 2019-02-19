from tornado import ioloop

from app import app

if __name__ == "__main__":
    app.listen(8888)
    ioloop.IOLoop.current().start()
