# -*- coding: utf-8 -*-
from google.appengine.ext import db

from common import RequestHandler, App
from models import Shop
from geocoder import Geocoder
from math import floor, sqrt

apikey = 'ABQIAAAAS2GR3nbO3xhKL2p1o_b5fBRPHsmlLL6wcQezZRl8E8AtCCqk4RSKdN0PdalrWPuHCQa-kH-nLv0s9Q'

# 1度あたりの距離
# http://ja.wikipedia.org/wiki/%E7%B7%AF%E5%BA%A6
# http://ja.wikipedia.org/wiki/%E7%B5%8C%E5%BA%A6
# 緯度１秒の長さ(緯度35度上) 約30.8m
# 経度１秒の長さ(緯度35度上) 約25m
dx_unit = 30.8 * 3600
dy_unit = 25.0 * 3600
def calc_distance(shop, coord):
    dx = floor(((shop.geo.lon - float(coord['lng'])) * dx_unit) + 0.5) / 1000
    dy = floor(((shop.geo.lat - float(coord['lat'])) * dy_unit) + 0.5) / 1000
    distance = floor(sqrt(dx*dx + dy*dy) * 1000 + 0.5) / 1000
    return {
        'dx': abs(dx),
        'dy': abs(dy),
        'label_x': '東に' if dx > 0 else '西に',
        'label_y': '北に' if dy > 0 else '南に',
        'distance': distance,
    }

def mapurl(lat, lng):
    url = 'http://www.google.co.jp/m/search?output=html&site=maps&q=%s,%s'
    return url % (lat, lng)

class SearchPage(RequestHandler):
    def get(self):
        #self.render_response('mobile/search.html', {}, 'shift_jis')
        self.render_response('mobile/search.html', {})

    def post(self):
        lnd = self.request.get('lnd')
        if lnd:
            geo = Geocoder(apikey=apikey)
            lnd_coord = geo.geocode(location=lnd)
            if lnd_coord:
                shops = Shop.all()
                shops = [
                    (shop,
                     calc_distance(shop, lnd_coord),
                     mapurl(shop.geo.lat, shop.geo.lon)
                    ) for shop in shops
                ]
                shops.sort(key=lambda k: k[1]['distance'])
                self.render_response('mobile/search_result.html', {
                    'lnd': lnd,
                    'lnd_map': mapurl(lnd_coord['lat'], lnd_coord['lng']),
                    'shops': shops[0:30]
                })
            else:
                self.response.out.write('not found')
        else:
            self.redirect('/m/search')

class MotiPage(RequestHandler):
    def get(self):
        self.redirect('/m/search')

if __name__ == "__main__":
    app = App([('/m/search', SearchPage),
               ('/moti.cgi', MotiPage),
              ])
    app.run()

