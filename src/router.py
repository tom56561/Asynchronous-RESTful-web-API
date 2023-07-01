import tornado.web
from MainHandler import MainHandler
from GuidHandler import GUIDHandler

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/guid/([A-Fa-f0-9]{32})", GUIDHandler),
        (r"/guid", GUIDHandler),
    ])