import unittest
from unittest.mock import MagicMock, patch
import tornado.testing
from tornado.testing import gen_test
import json
from src.app import make_app
from src.database import Database
from src.cache import Cache

class TestGUIDHandler(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        self.mock_db = MagicMock(spec=Database)
        self.mock_cache = MagicMock(spec=Cache)
        return make_app(db=self.mock_db, cache=self.mock_cache)

    @gen_test
    def test_get(self):
        """
        Test case for HTTP GET request to retrieve a GUID.
        It tests two scenarios:
        1. Getting a non-existing GUID should return a 404 status code.
        2. Getting an existing GUID should return a 200 status code and the correct metadata.
        """
        guid = "FA3A9A3A3A3A3A3A3A3A3A3A3A3A3A3A"
        metadata = {'guid': guid, 'user': 'test_user', 'expire': 1692444800}

        # Test getting a non-existing GUID
        self.mock_cache.get.return_value = None
        self.mock_db.get_guid.return_value = None   
        response = yield self.http_client.fetch(self.get_url(f"/guid/{guid}"), method="GET", raise_error=False)
        self.assertEqual(response.code, 404)

        # Test getting an existing GUID
        self.mock_cache.get.return_value = metadata
        response = yield self.http_client.fetch(self.get_url(f"/guid/{guid}"), method="GET", raise_error=False)
        self.assertEqual(response.code, 200)
        self.assertEqual(json.loads(response.body), metadata)

    @gen_test
    def test_post(self):
        """
        Test case for HTTP POST request to create a new GUID.
        It tests two scenarios:
        1. Creating a new GUID with valid data should return a 200 status code.
        2. Creating a new GUID with invalid data should return a 400 status code.
        """
        self.mock_db.create_guid.return_value = True

        # Test creating a new GUID
        body = json.dumps({"user": "test_user", "expire": "1692444800"})
        response = yield self.http_client.fetch(self.get_url("/guid"), method="POST", body=body, raise_error=False)
        self.assertEqual(response.code, 200)

        # Test creating a new GUID with invalid data
        body = json.dumps({"user": "test_user", "expire": "invalid"})
        response = yield self.http_client.fetch(self.get_url("/guid"), method="POST", body=body, raise_error=False)
        self.assertEqual(response.code, 400)

    @gen_test
    def test_delete(self):
        """
        Test case for HTTP DELETE request to delete a GUID.
        It tests two scenarios:
        1. Deleting an existing GUID should return a 204 status code.
        2. Deleting a non-existing GUID should return a 404 status code.
        """
        guid = "FA3A9A3A3A3A3A3A3A3A3A3A3A3A3A3A"

        # Test deleting an existing GUID
        self.mock_db.delete_guid.return_value = True
        response = yield self.http_client.fetch(self.get_url(f"/guid/{guid}"), method="DELETE")
        self.assertEqual(response.code, 204)

        # Test deleting a non-existing GUID
        self.mock_db.delete_guid.return_value = False
        response = yield self.http_client.fetch(self.get_url(f"/guid/{guid}"), method="DELETE", raise_error=False)
        self.assertEqual(response.code, 404)

    @gen_test
    def test_patch(self):
        """
        Test case for HTTP PATCH request to update a GUID.
        It tests two scenarios:
        1. Updating a non-existing GUID should return a 500 status code.
        2. Updating an existing GUID should return a 200 status code.
        """
        guid = "FA3A9A3A3A3A3A3A3A3A3A3A3A3A3A3A"
        metadata = {'guid': guid, 'user': 'test_user', 'expire': 1692444800}

        # Test updating a non-existing GUID
        self.mock_db.update_guid.return_value = False
        body = json.dumps({"user": "updated_user", "expire": "1692444800"})
        response = yield self.http_client.fetch(self.get_url(f"/guid/{guid}"), method="PATCH", body=body, raise_error=False)
        self.assertEqual(response.code, 500)

        # Test updating an existing GUID
        self.mock_db.get_guid.return_value = metadata
        self.mock_db.update_guid.return_value = True
        body = json.dumps({"user": "updated_user", "expire": "1692444800"})
        response = yield self.http_client.fetch(self.get_url(f"/guid/{guid}"), method="PATCH", body=body, raise_error=False)
        self.assertEqual(response.code, 200)
    
    @gen_test
    def test_post_server_error(self):
        """
        Test case for HTTP POST request when there's a server error during GUID creation.
        It tests if a 500 status code is returned when there's a server error during GUID creation.
        """
        self.mock_db.create_guid.return_value = False
        body = json.dumps({"user": "test_user", "expire": "1692444800"})
        response = yield self.http_client.fetch(self.get_url(f"/guid"), method="POST", body=body, raise_error=False)
        self.assertEqual(response.code, 500)
    
    @gen_test
    def test_patch_server_error(self):
        """
        Test case for HTTP PATCH request when there's a server error during GUID update.
        It tests if a 500 status code is returned when there's a server error during GUID update.
        """
        guid = "FA3A9A3A3A3A3A3A3A3A3A3A3A3A3A3A"
        metadata = {'guid': guid, 'user': 'test_user', 'expire': 1692444800}
        self.mock_db.get_guid.return_value = metadata
        self.mock_db.update_guid.return_value = False
        body = json.dumps({"user": "updated_user", "expire": "1692444800"})
        response = yield self.http_client.fetch(self.get_url(f"/guid/{guid}"), method="PATCH", body=body, raise_error=False)
        self.assertEqual(response.code, 500)

    @gen_test
    def test_delete_no_guid(self):
        """
        Test case for HTTP DELETE request when the GUID is not provided.
        It tests if a 400 status code is returned when the GUID is not properly provided.
        """
        self.mock_db.delete_guid.return_value = True
        response = yield self.http_client.fetch(self.get_url(f"/guid"), method="DELETE", raise_error=False)
        self.assertEqual(response.code, 400)

    @gen_test    
    def test_post_invalid_data(self):
        """
        Test case for HTTP POST request with invalid data for GUID creation.
        It tests if a 400 status code is returned and the appropriate error messages are included in the response body
        when invalid data is provided for GUID creation.
        """
        self.mock_db.create_guid.return_value = True
        body = json.dumps({"user": 123, "expire": "invalid_timestamp"})
        response = yield self.http_client.fetch(self.get_url(f"/guid"), method="POST", body=body, raise_error=False)
        self.assertEqual(response.code, 400)
        self.assertIn(b'"user": "User must be a string."', response.body)
        self.assertIn(b'"expire": "Expire must be a string of digits."', response.body)

    @gen_test
    def test_patch_invalid_data(self):
        """
        Test case for HTTP PATCH request with invalid data for GUID update.
        It tests if a 400 status code is returned and the appropriate error messages are included in the response body
        when invalid data is provided for GUID update.
        """
        guid = "FA3A9A3A3A3A3A3A3A3A3A3A3A3A3A3A"
        metadata = {'guid': guid, 'user': 'test_user', 'expire': 1692444800}
        self.mock_db.get_guid.return_value = metadata
        self.mock_db.update_guid.return_value = True
        body = json.dumps({"user": 123, "expire": "invalid_timestamp"})
        response = yield self.http_client.fetch(self.get_url(f"/guid/{guid}"), method="PATCH", body=body, raise_error=False)
        self.assertEqual(response.code, 400)
        self.assertIn(b'"user": "User must be a string."', response.body)
        self.assertIn(b'"expire": "Expire must be a string of digits."', response.body)

    @gen_test
    def test_post_missing_user(self):
        """
        Test case for HTTP POST request with missing user field.
        It tests if a 400 status code is returned and an appropriate error message is included in the response body
        when the user field is missing in the request body for GUID creation.
        """
        self.mock_db.create_guid.return_value = True
        body = json.dumps({"expire": "1692444800"})
        response = yield self.http_client.fetch(self.get_url("/guid"), method="POST", body=body, raise_error=False)
        self.assertEqual(response.code, 400)
        self.assertIn(b'"user": "User field is required."', response.body)

    @gen_test
    def test_post_invalid_expire(self):
        """
        Test case for HTTP POST request with invalid expire field.
        It tests if a 400 status code is returned and an appropriate error message is included in the response body
        when the expire field is not a string of digits in the request body for GUID creation.
        """
        self.mock_db.create_guid.return_value = True
        body = json.dumps({"user": "test_user", "expire": "invalid_timestamp"})
        response = yield self.http_client.fetch(self.get_url("/guid"), method="POST", body=body, raise_error=False)
        self.assertEqual(response.code, 400)
        self.assertIn(b'"expire": "Expire must be a string of digits."', response.body)

    @gen_test
    def test_delete_non_existing_guid(self):
        """
        Test case for HTTP DELETE request for a non-existing GUID.
        It tests if a 404 status code is returned and an appropriate error message is included in the response body
        when attempting to delete a non-existing GUID.
        """
        guid = "FA3A9A3A3A3A3A3A3A3A3A3A3A3A3A3A"
        self.mock_db.delete_guid.return_value = False
        response = yield self.http_client.fetch(self.get_url(f"/guid/{guid}"), method="DELETE", raise_error=False)
        self.assertEqual(response.code, 404)
        self.assertIn(b'GUID not found.', response.body)

