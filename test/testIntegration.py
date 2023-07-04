import unittest
import json
import asyncio
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.httpclient import AsyncHTTPClient

from src.app import make_app
from src.database import Database
from src.cache import Cache

class TestGUIDIntegration(AsyncHTTPTestCase):
    def get_app(self):
        return make_app(db=Database(), cache=Cache())

    @gen_test
    async def test_async_behaviour_get(self):
        # Prepare a bunch of urls to hit your API
        guids = ["FA3A9A3A3A3A3A3A3A3A3A3A3A3A3A3A" for _ in range(1)]
        urls = [self.get_url(f"/guid/{guid}") for guid in guids]

        # Prepare the http_client
        http_client = AsyncHTTPClient()

        # Prepare all the requests but do not start them
        fetch_coroutines = [http_client.fetch(url, method="GET", raise_error=False) for url in urls]

        # Start all requests concurrently (not one after the other)
        responses = await asyncio.gather(*fetch_coroutines)

        # Make assertions on the responses
        for response in responses:
            self.assertIn(response.code, [200, 404])  # If the guid exists, it should return 200. If not, 404.

    