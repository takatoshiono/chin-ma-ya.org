from common import RequestHandler, App
from models import Shop

class ShopPage(RequestHandler):
    def post(self):
        id = self.request.get('id')
        shop = Shop.all().filter('id = ', int(id)).get()

        if shop:
            shop.delete()
            self.response.out.write('%s deleted.' % self.request.get('name'))
        else:
            self.response.out.write('%s not found' % self.request.get('name'))

if __name__ == '__main__':
    app = App([('/admin/delete/shop', ShopPage),
              ])
    app.run()

