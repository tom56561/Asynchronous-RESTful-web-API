import unittest
import json
import asyncio
import time
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.httpclient import AsyncHTTPClient

from src.app import make_app
from src.database import Database
from src.cache import Cache

class TestGUIDIntegration(AsyncHTTPTestCase):
    def get_app(self):
        return make_app(db=Database(), cache=Cache())
    
    @gen_test
    async def test_async_behaviour_post(self):
        guids = ["FA3A9A3A3A3A3A3A3A3A3A3A3A3A3A3" + str(i) for i in range(100)]

        http_client = AsyncHTTPClient()

        fetch_coroutines = [
            http_client.fetch(
                self.get_url(f"/guid/{guid}"),
                method = "POST",
                body = json.dumps({
                    "guid": guid,
                    "expire": int(time.time()) + 3600,
                    "user": "Test user"
                }),
                headers = {"Content-Type": "application/json"},  # Specify that you're sending JSON
                raise_error=False
            ) 
            for guid in guids
        ]

        responses = await asyncio.gather(*fetch_coroutines)

        for response in responses:
            self.assertEqual(response.code, 201)

    @gen_test
    async def test_async_behaviour_get(self):
        guids = ["FA3A9A3A3A3A3A3A3A3A3A3A3A3A3A3" + str(i) for i in range(100)]
        urls = [self.get_url(f"/guid/{guid}") for guid in guids]

        http_client = AsyncHTTPClient()

        fetch_coroutines = [http_client.fetch(url, method="GET", raise_error=False) for url in urls]

        responses = await asyncio.gather(*fetch_coroutines)

        for response in responses:
            self.assertIn(response.code, [200, 404])

    @gen_test
    async def test_async_behaviour_put(self):
        guids = ["FA3A9A3A3A3A3A3A3A3A3A3A3A3A3A3" + str(i) for i in range(100)]
        http_client = AsyncHTTPClient()

        put_coroutines = [
            http_client.fetch(
                self.get_url(f"/guid/{guid}"),
                method="PATCH",
                body=json.dumps({
                    "guid": guid,
                    "expire": int(time.time()) + 7200,
                    "user": f"Updated user {i}"
                }),
                headers={"Content-Type": "application/json"},
                raise_error=False
            )
            for i, guid in enumerate(guids)
        ]

        responses = await asyncio.gather(*put_coroutines)

        for response in responses:
            self.assertEqual(response.code, 200)

    @gen_test
    async def test_async_behaviour_delete(self):
        guids = ["FA3A9A3A3A3A3A3A3A3A3A3A3A3A3A3" + str(i) for i in range(100)]
        http_client = AsyncHTTPClient()

        delete_coroutines = [
            http_client.fetch(
                self.get_url(f"/guid/{guid}"),
                method="DELETE",
                raise_error=False
            )
            for guid in guids
        ]

        responses = await asyncio.gather(*delete_coroutines)

        for response in responses:
            self.assertEqual(response.code, 204)

        get_coroutines = [
            http_client.fetch(
                self.get_url(f"/guid/{guid}"),
                method="GET",
                raise_error=False
            )
            for guid in guids
        ]

        responses = await asyncio.gather(*get_coroutines)

        for response in responses:
            self.assertEqual(response.code, 404)