from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient('db', 27017)
        self.db = self.client['guids_data']

    def get_guid(self, guid):
        try:
            collection = self.db['guids']
            result = collection.find_one({'_id': guid})
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def create_guid(self, guid, metadata):
        try:
            collection = self.db['guids']
            result = collection.insert_one({'_id': guid, **metadata})
            return result.acknowledged
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def update_guid(self, guid, metadata):
        # implement updating guid in the database
        pass

    def delete_guid(self, guid):
        # implement deleting guid from the database
        pass

