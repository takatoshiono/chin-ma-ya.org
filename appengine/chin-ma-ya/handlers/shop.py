import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.ext import webapp

from common import RequestHandler, App
from models import Shop

class ListPage(RequestHandler):
    def get(self):
        shops = Shop.all().order('area')
        template_vars = { 'object_list': shops }
        self.render_response('shop/shop_list.html', template_vars)

class KMLPage(RequestHandler):
    def get(self):
        shops = Shop.all().order('area')
        template_vars = {'object_list': shops}
        self.response.headers['Content-Type'] = 'text/plain; charset=utf-8'
        self.render_response('shop/shop_kml.xml', template_vars)

class DetailByIdPage(RequestHandler):
    def get(self, id):
        shop = Shop.all().filter('id = ', int(id)).get()
        template_vars = { 'object': shop }
        self.render_response('shop/shop_detail.html', template_vars)

class DetailPage(RequestHandler):
    def get(self, key):
        shop = db.get(key)
        template_vars = { 'object': shop }
        self.render_response('shop/shop_detail.html', template_vars)

if __name__ == "__main__":
    app = App([('/shops/?', ListPage),
               ('/shops/kml/?', KMLPage),
               ('/shops/(?P<id>\d+)/?', DetailByIdPage),
               ('/shops/(?P<key>.+)/?', DetailPage),
              ])
    app.run()

