from datetime import datetime
from google.appengine.ext import bulkload
from google.appengine.api import datastore_types

class AreaLoader(bulkload.Loader):
    def __init__(self):
        bulkload.Loader.__init__(self, 'Area',
                                 [('id', int),
                                  ('name', str),
                                  ('url', datastore_types.Link),
                                  ('updated_at', lambda x: datatime.strptime(x, '%Y-%m-%d %H:%M:$S')),
                                  ('created_at', lambda x: datatime.strptime(x, '%Y-%m-%d %H:%M:$S')),
                                 ])

if __name__ == '__main__':
    bulkload.main(AreaLoader())

