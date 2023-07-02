import redis
import json
import time

class Cache:
    """
    A class used to interact with a Redis cache for caching GUID data.
    """

    def __init__(self):
        """Initializes a new instance of the Cache class."""
        self.client = redis.Redis(host='redis', port=6379, db=0)
        self.default_ttl = 3600  # default TTL of 1 hour

    def get(self, guid):
        """Retrieves GUID data from the cache."""
        result = self.client.get(guid)
        if result:
            return json.loads(result)
        else:
            return None

    def set(self, guid, value):
        """Stores GUID data in the cache with an appropriate time-to-live."""
        ttl = self.default_ttl
        remaining_time = value['expire'] - int(time.time())

        if remaining_time < ttl:
            ttl = remaining_time
        self.client.set(guid, json.dumps(value), ex=ttl)

    def delete(self, guid):
        """Deletes GUID data from the cache."""
        self.client.delete(guid)