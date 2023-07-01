import tornado.web
from mainHandler import MainHandler
from guidHandler import GUIDHandler

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/guid/([A-Fa-f0-9]{32})", GUIDHandler),
        (r"/guid", GUIDHandler),
    ])