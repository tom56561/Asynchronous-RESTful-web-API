import tornado.web
from guid_handler import GUIDHandler

def make_app():
    return tornado.web.Application([
        (r"/guid/([A-Fa-f0-9]{32})", GUIDHandler),
        (r"/guid", GUIDHandler),
    ])