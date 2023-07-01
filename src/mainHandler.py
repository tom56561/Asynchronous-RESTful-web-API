import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Welcome to the GUID API. Available routes: /guid")
