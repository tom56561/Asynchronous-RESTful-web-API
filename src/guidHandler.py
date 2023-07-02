import tornado.web
from database import Database
from cache import Cache
import time
import uuid
import time
import json

class GUIDHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.db = Database()
        self.cache = Cache()
    
    def validate_input(self, data):
        user = data.get('user')
        expire = data.get('expire')

        errors = {}

        if user is not None and not isinstance(user, str):
            errors['user'] = 'User must be a string.'

        if expire is not None:
            if not expire.isdigit():
                errors['expire'] = 'Expire must be a string of digits.'
            elif int(expire) <= int(time.time()):
                errors['expire'] = 'Expire must be a future Unix timestamp.'

        return errors

    def check_guid(self, guid):
        if not guid:
            self.send_error(400, message="GUID not provided.")
            return False
        return True

    async def get(self, guid=None):
        if not self.check_guid(guid):
            return

        # Try getting the metadata from the cache first
        metadata = self.cache.get(guid)
        if metadata is None:
            # If the metadata is not in the cache, get it from the database
            metadata = self.db.get_guid(guid)

            # If the metadata is still None after querying the database, the GUID does not exist
            if metadata is None:
                self.set_status(404)
                self.write({'error': 'GUID not found or has expired.'})
                return

            # Put the metadata in the cache for future use
            self.cache.set(guid, metadata)

        self.write(metadata)


    async def post(self, guid=None):
        data = json.loads(self.request.body)

        errors = self.validate_input(data)
        if errors:
            self.set_status(400)
            self.write({'errors': errors})
            return

        user = data.get('user')
        # defaults to 30 days from now and store it as Unix time
        expire = int(data.get('expire', int(time.time()) + 30*24*60*60))
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
        if not self.check_guid(guid):
            return
        
        result = self.db.delete_guid(guid)
        if result:
            self.cache.delete(guid)
            self.set_status(204)  # No content
        else:
            self.set_status(500)
            self.write({'error': 'Failed to delete GUID.'})

    async def patch(self, guid=None):
        if not self.check_guid(guid):
            return
        
        errors = self.validate_input(data)
        if errors:
            self.set_status(400)
            self.write({'errors': errors})
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