from datetime import datetime
from google.appengine.ext import bulkload
from google.appengine.api import datastore_types
from models import Area

class ShopLoader(bulkload.Loader):
    def __init__(self):
        bulkload.Loader.__init__(self, 'Shop',
                                 [('id', int),
                                  ('area', self.get_area_key),
                                  ('name', str),
                                  ('address', str),
                                  ('geo', datastore_types.GeoPt),
                                  ('extra', datastore_types.Text),
                                  ('updated_at', lambda x: datatime.strptime(x, '%Y-%m-%d %H:%M:$S')),
                                  ('created_at', lambda x: datatime.strptime(x, '%Y-%m-%d %H:%M:$S')),
                                 ])

    def get_area_key(self, name):
        area = Area.all().filter('name = ', name).get()
        if area:
            return area.key()
        else:
            return ''

if __name__ == '__main__':
    bulkload.main(ShopLoader())

