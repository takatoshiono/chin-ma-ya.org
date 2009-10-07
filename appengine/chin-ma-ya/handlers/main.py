from common import RequestHandler, App
from models import Shop

class MainPage(RequestHandler):
    def get(self):
        self.redirect("http://chinma-ya.appspot.com/", True)
        #new_shops = Shop.gql('ORDER BY id DESC').fetch(limit=10)
        #self.render_response('index.html', {
        #    'new_shops': new_shops
        #    })

if __name__ == "__main__":
    app = App([('/', MainPage),
              ])
    app.run()

