import tornado.web
from .database import Database
from .cache import Cache
import time
import uuid
import time
import json

class GUIDHandler(tornado.web.RequestHandler):
    """
    Handles HTTP requests related to GUIDs (Globally Unique Identifiers). 
    Works with a Database class for storing GUID data and a Cache class for caching GUID data.
    """

    def initialize(self, db, cache):
        """Initializes a new instance of the GUIDHandler."""
        self.db = db
        self.cache = cache
    
    def validate_input(self, data):
        """
        Validates input data for a new or existing GUID. 
        Returns a dictionary mapping field names to error messages if there are errors.
        """
        user = data.get('user')
        expire = data.get('expire')

        errors = {}
        if user is None and expire is None:
            errors['invalid'] = "Input data should not be empty."
            return errors

        if user is None:
            errors['user'] = 'User field is required.'
        elif not isinstance(user, str):
            errors['user'] = 'User must be a string.'

        if expire is not None:
            if not str(expire).isdigit():
                errors['expire'] = 'Expire must be a string or number of digits.'
            elif int(expire) <= int(time.time()):
                errors['expire'] = 'Expire must be a future Unix timestamp.'

        return errors

    def check_guid(self, guid):
        """
        Checks whether a GUID has been provided. If not, sends a 400 error response and returns False.
        """
        if not guid:
            self.set_status(400)
            self.write({'error': 'GUID not provided.'})
            return False
        return True

    async def get(self, guid=None):
        """
        Handles HTTP GET requests for a GUID. If a GUID is provided, it attempts to retrieve its data.
        If the GUID does not exist in the database, sends a 404 error response.
        """
        if not self.check_guid(guid):
            return

        metadata = self.cache.get(guid)
        if metadata is None:
            metadata = self.db.get_guid(guid)

            if metadata is None:
                self.set_status(404)
                self.write({'error': 'GUID not found or has expired.'})
                return

            self.cache.set(guid, metadata)

        self.write(metadata)


    async def post(self, guid=None):
        """
        Handles HTTP POST requests to create a new GUID or update an existing one. 
        If the input data is valid, it creates or updates the GUID, else it sends a 400 error response.
        """
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
            'guid':guid,
            'user': user,
            'expire': expire
        }

        result = self.db.create_guid(guid, metadata)
        if result:
            self.cache.set(guid, metadata)
            self.set_status(201)
            self.write(metadata)
        else:
            self.set_status(500)
            self.write({'error': 'Failed to create GUID.'})

    async def delete(self, guid=None):
        """
        Handles HTTP DELETE requests to delete a GUID. If a GUID is provided, it deletes it.
        """
        if not self.check_guid(guid):
            return
        
        result = self.db.delete_guid(guid)
        if result:
            self.cache.delete(guid)
            self.set_status(204)  # No content
        else:
            self.set_status(404)
            self.write({'error': 'GUID not found.'})

    async def patch(self, guid=None):
        """
        Handles HTTP PATCH requests to update an existing GUID. 
        If a GUID is provided and the input data is valid, it updates the GUID, else it sends a 400 error response.
        """
        if not self.check_guid(guid):
            return
        
        data = json.loads(self.request.body)
        errors = self.validate_input(data)
        if errors:
            self.set_status(400)
            self.write({'errors': errors})
            return
    
        if data.get('expire') is not None:
            data['expire'] = int(data.get('expire'))
        result = self.db.update_guid(guid, data)
        if result:
            updated_data = self.db.get_guid(guid)
            self.cache.set(guid, updated_data)
            self.write(updated_data)
        else:
            self.set_status(500)
            self.write({'error': 'Failed to update GUID.'})