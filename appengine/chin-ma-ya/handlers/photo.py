from google.appengine.api import users, images
from google.appengine.ext import db

from common import RequestHandler, App
from models import Shop, Photo

class ListPage(RequestHandler):
    def get(self):
        photo_list = Photo.all().order('-updated_at')
        template_vars = { 'object_list': photo_list }
        self.render_response('photo/photo_list.html', template_vars)

class EditPage(RequestHandler):
    def get(self, key):
        shops = Shop.all().order('area')
        template_vars = { 'shops': shops }
        if key:
            template_vars['object'] = db.get(key)
        self.render_response('photo/photo_edit.html', template_vars)

    def post(self, *args):
        if self.request.get('shop'):
            shop = db.get(self.request.get('shop'))
        else:
            shop = None

        if self.request.get('key'):
            photo = db.get(self.request.get('key'))
        else:
            img = self.request.body_file.vars['image']
            photo = Photo(user = users.get_current_user(),
                          shop = shop,
                          title = self.request.get('title'),
                          image = self.request.get('image'),
                          mime_type = img.headers['content-type'],
                          filename = img.filename,
                          size = len(self.request.get('image')),
                          )
        photo.put()
        self.redirect('/photo')

class Image(RequestHandler):
    def get(self):
        photo = db.get(self.request.get('key'))
        if photo.image:
            if self.request.get('resize'):
                width, height = self.request.get('width', 0), self.request.get('height', 0)
                img = images.Image(photo.image)
                img.resize(int(width), int(height))
                self.response.headers['Content-Type'] = 'image/png'
                self.response.out.write(img.execute_transforms())
            else:
                self.response.headers['Content-Type'] = str(photo.mime_type)
                self.response.out.write(photo.image)
        else:
            self.response.out.write('')

if __name__ == "__main__":
    app = App([('/photo', ListPage),
               ('/photo/edit/?(?P<key>.*)', EditPage),
               ('/photo/img', Image),
              ])
    app.run()

