import tornado.ioloop
import tornado.web
import pymongo
import uuid
import json
from datetime import datetime, timedelta  # add this line



# Setup MongoDB client
client = pymongo.MongoClient('db', 27017)
db = client.guid_db
collection = db.guid_collection

class MainHandler(tornado.web.RequestHandler):
    def post(self, guid=None):
        # Extract metadata from request body
        body = json.loads(self.request.body)
        user = body.get('user')
        expire = body.get('expire')
        if not guid:
            # Generate new GUID if not provided
            guid = str(uuid.uuid4()).upper().replace('-', '')

        # Create document
        document = {
            "_id": guid,
            "user": user,
            "expire": expire if expire else str(int((datetime.now() + timedelta(days=30)).timestamp()))
        }
        # Store in MongoDB and Redis
        collection.insert_one(document)

        self.write(document)

def make_app():
    return tornado.web.Application([
        (r"/guid/?([a-fA-F0-9]{32})?", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()