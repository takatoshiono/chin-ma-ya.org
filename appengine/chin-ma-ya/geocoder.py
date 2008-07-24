# -*- coding: utf-8 -*-

import urllib
import xml.dom.minidom
from google.appengine.api import urlfetch

class Geocoder(object):
    def __init__(self, apikey, host='maps.google.com'):
        self.apikey = apikey
        self.host = host

    def geocode(self, location):
        if isinstance(location, unicode):
            location = location.encode('utf-8')
        url = 'http://%s/maps/geo?q=%s&output=xml&key=%s' % (self.host, urllib.quote_plus(location), self.apikey)
        res = urlfetch.fetch(url)
        dom = xml.dom.minidom.parseString(res.content)
        coordinates = dom.getElementsByTagName('coordinates')
        if coordinates:
            lng, lat, z = coordinates[0].firstChild.data.split(',')
            return { 'lat': lat, 'lng': lng }
        else:
            return

