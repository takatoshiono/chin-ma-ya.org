from common import RequestHandler, App

class MainPage(RequestHandler):
    def get(self):
        self.render_response('index.html', {})

if __name__ == "__main__":
    app = App([('/', MainPage),
              ])
    app.run()

