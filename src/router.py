import tornado.web
from .mainHandler import MainHandler
from .guidHandler import GUIDHandler
from .database import Database
from .cache import Cache

def make_app(db=None, cache=None):
    # If no mock instances were provided, create real ones
    if db is None:
        db = Database()
    if cache is None:
        cache = Cache()

    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/guid/([A-F0-9]{32})", GUIDHandler, dict(db=db, cache=cache)),
        (r"/guid/?", GUIDHandler, dict(db=db, cache=cache)),
    ])