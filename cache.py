import redis
import json

class Cache:
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379)

    def get(self, guid):
        result = self.client.get(guid)
        if result:
            return json.loads(result)
        else:
            return None

    def set(self, guid, value):
        self.client.set(guid, json.dumps(value))

    def delete(self, guid):
        self.client.delete(guid)