from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['your_database']

    def get_guid(self, guid):
        # implement getting guid from the database
        pass

    def create_guid(self, guid, metadata):
        # implement creating guid in the database
        pass

    def update_guid(self, guid, metadata):
        # implement updating guid in the database
        pass

    def delete_guid(self, guid):
        # implement deleting guid from the database
        pass