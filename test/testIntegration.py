import uuid
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
    GUIDS = [uuid.uuid4().hex.upper() for _ in range(100)]

    def get_app(self):
        return make_app(db=Database(), cache=Cache())
    
    @gen_test
    async def test_async_guid_lifecycle(self):
        http_client = AsyncHTTPClient()
        
        for guid in self.GUIDS:
            # POST
            response = await http_client.fetch(
                self.get_url(f"/guid/{guid}"),
                method = "POST",
                body = json.dumps({
                    "guid": guid,
                    "expire": int(time.time()) + 3600,
                    "user": "Test user"
                }),
                headers = {"Content-Type": "application/json"},  
                raise_error=False
            )
            self.assertEqual(response.code, 201)
            
            # GET
            response = await http_client.fetch(
                self.get_url(f"/guid/{guid}"),
                method = "GET",
                raise_error=False
            )
            self.assertEqual(response.code, 200)

            # PATCH
            response = await http_client.fetch(
                self.get_url(f"/guid/{guid}"),
                method="PATCH",
                body=json.dumps({
                    "guid": guid,
                    "expire": int(time.time()) + 7200,
                    "user": "Updated user"
                }),
                headers={"Content-Type": "application/json"},
                raise_error=False
            )
            self.assertEqual(response.code, 200)

            # DELETE
            response = await http_client.fetch(
                self.get_url(f"/guid/{guid}"),
                method="DELETE",
                raise_error=False
            )
            self.assertEqual(response.code, 204)

            # GET after DELETE to check that the resource was deleted
            response = await http_client.fetch(
                self.get_url(f"/guid/{guid}"),
                method="GET",
                raise_error=False
            )
            self.assertEqual(response.code, 404)
