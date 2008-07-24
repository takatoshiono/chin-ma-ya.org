from google.appengine.api import users
from google.appengine.ext import db

from common import RequestHandler, App
from models import Shop, BlogEntry
from forms import BlogEntryForm

class ListPage(RequestHandler):
    def get(self):
        entries = BlogEntry.all().order('-updated_at')
        template_vars = { 'object_list': entries }
        self.render_response('blog/blog_list.html', template_vars)

class EditPage(RequestHandler):
    def get(self, key):
        shops = Shop.all().order('area')
        template_vars = { 'shops': shops }
        if key:
            entry = db.get(key)
            if entry.user == users.get_current_user():
                template_vars['object'] = entry
                self.render_response('blog/blog_edit.html', template_vars)
            else:
                self.redirect('/blog/edit')
        else:
            self.render_response('blog/blog_edit.html', template_vars)

    def post(self, *args):
        form = BlogEntryForm(data=self.request.POST)
        if form.is_valid():
            shop = db.get(self.request.get('shop'))
            if self.request.get('key'):
                entry = db.get(self.request.get('key'))
                entry.shop = shop
                entry.title = self.request.get('title')
                entry.body = self.request.get('body')
            else:
                entry = BlogEntry(user = users.get_current_user(),
                                  shop = shop,
                                  title = self.request.get('title'),
                                  body = self.request.get('body'),
                                  )
            entry.put()
            self.redirect('/blog')
        else:
            shops = Shop.all().order('area')
            template_vars = { 'shops': shops, 'form': form }
            self.render_response('blog/blog_edit.html', template_vars)

class PermalinkPage(RequestHandler):
    def get(self, key):
        template_vars = {
            'object': db.get(key),
        }
        self.render_response('blog/blog_detail.html', template_vars)

if __name__ == "__main__":
    app = App([('/blog', ListPage),
               ('/blog/edit/?(?P<key>.*)', EditPage),
               ('/blog/(?P<key>.+)', PermalinkPage),
              ])
    app.run()

