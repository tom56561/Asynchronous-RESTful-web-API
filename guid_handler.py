import tornado.web
from database import Database
from cache import Cache

class GUIDHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.db = Database()
        self.cache = Cache()

    async def get(self, guid=None):
        # implement your GET logic here
        pass

    async def post(self, guid=None):
        # implement your POST logic here
        pass

    async def delete(self, guid=None):
        # implement your DELETE logic here
        pass