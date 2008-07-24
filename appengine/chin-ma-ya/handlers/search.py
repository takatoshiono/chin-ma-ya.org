from common import RequestHandler, App

class SearchPage(RequestHandler):
    def get(self):
        self.render_response('search/index.html', {})

if __name__ == "__main__":
    app = App([('/search', SearchPage),
              ])
    app.run()

