import unittest
import tornado.ioloop
import tornado.testing
import json
from src.app import make_app 

class TestApp(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    def test_post(self):
        post_data = {"user": "Cylance, Inc."}
        response = self.fetch("/guid", method="POST", body=json.dumps(post_data))
        # Expected HTTP status code is 200 for successful POST
        self.assertEqual(response.code, 200)
        response_body = json.loads(response.body)
        # The response should contain a valid guid
        self.assertEqual(len(response_body.get('guid')), 32)
        self.assertEqual(response_body.get('user'), post_data.get('user'))

if __name__ == "__main__":
    unittest.main()
