from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from headspring import app

server = HTTPServer(WSGIContainer(app))
server.bind(8080)
server.start(0)  # Forks multiple sub-processes
IOLoop.current().start()
