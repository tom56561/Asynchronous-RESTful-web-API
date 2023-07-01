import redis
import json

class Cache:
    def __init__(self):
        self.client = redis.Redis(host='redis', port=6379, db=0)
        self.default_ttl = 3600  # default TTL of 1 hour

    def get(self, guid):
        result = self.client.get(guid)
        if result:
            return json.loads(result)
        else:
            return None

    def set(self, guid, value):
        ttl = self.default_ttl
        self.client.set(guid, json.dumps(value), ex=ttl)

    def delete(self, guid):
        self.client.delete(guid)