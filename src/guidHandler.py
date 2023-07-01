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
        if not guid:
            self.set_status(400)
            self.write({'error': 'GUID not provided.'})
            return

        # Try getting the metadata from the cache first
        metadata = self.cache.get(guid)
        if metadata is None:
            # If the metadata is not in the cache, get it from the database
            metadata = self.db.get_guid(guid)

            # If the metadata is still None after querying the database, the GUID does not exist
            if metadata is None:
                self.set_status(404)
                self.write({'error': 'GUID not found.'})
                return

            # Put the metadata in the cache for future use
            self.cache.set(guid, metadata)

        self.write(metadata)


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
        result = self.db.delete_guid(guid)
        if result:
            self.cache.delete(guid)
            self.set_status(204)  # No content
        else:
            self.set_status(500)
            self.write({'error': 'Failed to delete GUID.'})

    async def put(self, guid=None):
        if guid is None:
            self.set_status(400)
            self.write({'error': 'GUID must be provided for update.'})
            return

        data = json.loads(self.request.body)
        result = self.db.update_guid(guid, data)
        if result:
            updated_data = self.db.get_guid(guid)
            self.cache.set(guid, updated_data)
            self.write(updated_data)
        else:
            self.set_status(500)
            self.write({'error': 'Failed to update GUID.'})