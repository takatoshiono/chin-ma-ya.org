from google.appengine.ext import db
from common import RequestHandler, App
from models import Area

class AreaPage(RequestHandler):
    def post(self):
        id = self.request.get('id')
        area = Area.all().filter('id = ', id).get()

        op = ''
        if area:
            op = 'updated'
            area.name = self.request.get('name')
            area.url = self.request.get('url')
        else:
            op = 'created'
            area = Area(id = int(id),
                        name = self.request.get('name'),
                        url = self.request.get('url'),
                        )
        area.put()
        self.response.out.write('%s %s.' % (self.request.get('name'), op))

if __name__ == '__main__':
    app = App([('/admin/post/area', AreaPage),
              ])
    app.run()

