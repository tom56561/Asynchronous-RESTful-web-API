from pymongo import MongoClient
import time

class Database:
    """
    A class used to interact with a MongoDB database for managing GUIDs.
    """

    def __init__(self):
        """Initializes a new instance of the Database class."""
        self.client = MongoClient('db', 27017)
        self.db = self.client['guids_data']
        self.guids = self.db['guids']

    def get_guid(self, guid):
        """Fetches a GUID document from the MongoDB collection."""
        try:
            result = self.guids.find_one({'_id': guid, 'expire': {'$gt': int(time.time())}})
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def create_guid(self, guid, metadata):
        """Creates a new GUID document in the MongoDB collection."""
        try:
            result = self.guids.insert_one({'_id': guid, **metadata})
            return result.acknowledged
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def update_guid(self, guid, metadata):
        """Updates an existing GUID document in the MongoDB collection."""
        try:
            result = self.guids.update_one({'_id': guid}, {'$set': metadata})
            return result.acknowledged
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def delete_guid(self, guid):
        """Deletes a GUID document from the MongoDB collection."""
        try:
            result = self.guids.delete_one({'_id': guid})
            return result.acknowledged
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

