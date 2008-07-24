from google.appengine.api import users
from google.appengine.ext import db

from common import RequestHandler, App
from models import Profile
from forms import ProfileForm

class ProfilePage(RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            profile = Profile.all().filter('user =', user).get()
            template_vars = { 'profile': profile }
            self.render_response('profile/profile_detail.html', template_vars)
        else:
            self.redirect('/')

class EditPage(RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            profile = Profile.all().filter('user =', user).get()
            template_vars = { 'profile': profile }
            self.render_response('profile/profile_edit.html', template_vars)
        else:
            self.redirect('/')

    def post(self):
        form = ProfileForm(data=self.request.POST)
        if form.is_valid():
            user = users.get_current_user()
            username = self.request.get('username')
            #profile = Profile.all().filter('user !=', user).filter('username =', username).get()
            profile = Profile.all().filter('username =', username).get()
            if profile and profile.user != user:
                errors = { 'username_exists': ['%s is already exists'] }
                profile = { 'username': username }
                template_vars = { 'errors': errors, 'profile': profile }
                self.render_response('profile/profile_edit.html', template_vars)
            else:
                profile = Profile.all().filter('user =', user).get()
                if profile:
                    profile.username = username
                else:
                    profile = Profile(user = user,
                                      username = username,
                                      )
                profile.put()
                self.redirect('/profile')
        else:
            template_vars = { 'form': form }
            self.render_response('profile/profile_edit.html', template_vars)

if __name__ == '__main__':
        app = App([('/profile', ProfilePage),
                   ('/profile/edit', EditPage),
                   ])
        app.run()

