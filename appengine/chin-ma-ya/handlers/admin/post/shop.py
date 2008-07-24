from google.appengine.ext import db
from common import RequestHandler, App
from models import Area, Shop

class ShopPage(RequestHandler):
    def post(self):
        id = self.request.get('id')
        shop = Shop.all().filter('id = ', id).get()

        op = ''
        if shop:
            op = 'updated'
            shop.area = self.get_area_key(self.request.get('area'))
            shop.name = self.request.get('name')
            shop.address = self.request.get('address')
            shop.geo = db.GeoPt(lat = self.request.get('lat'),
                                lon = self.request.get('lon')),
            shop.extra = self.request.get('extra')
        else:
            op = 'created'
            shop = Shop(id = int(id),
                        area = self.get_area_key(self.request.get('area')),
                        name = self.request.get('name'),
                        address = self.request.get('address'),
                        geo = db.GeoPt(lat = self.request.get('lat'),
                                       lon = self.request.get('lon')),
                        extra = self.request.get('extra'),
                        )
        shop.put()
        self.response.out.write('%s %s.' % (self.request.get('name'), op))

    def get_area_key(self, name):
        area = Area.all().filter('name = ', name).get()
        if area:
            return area.key()
        else:
            return ''

if __name__ == '__main__':
    app = App([('/admin/post/shop', ShopPage),
              ])
    app.run()

