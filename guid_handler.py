import tornado.web
from database import Database
from cache import Cache
import uuid
import time
import json

class GUIDHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.db = Database()
        self.cache = Cache()

    async def get(self, guid=None):
        # implement your GET logic here
        pass

    async def post(self, guid=None):
        data = json.loads(self.request.body)
        user = data.get('user')
        expire = data.get('expire', time.time() + 30*24*60*60)  # defaults to 30 days from now
        guid = guid or uuid.uuid4().hex.upper()

        metadata = {
            'guid': guid,
            'user': user,
            'expire': expire
        }

        result = self.db.create_guid(guid, metadata)
        if result:
            self.cache.set(guid, metadata)
            self.write(metadata)
        else:
            self.set_status(500)
            self.write({'error': 'Failed to create GUID.'})

    async def delete(self, guid=None):
        # implement your DELETE logic here
        pass