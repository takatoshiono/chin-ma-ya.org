from google.appengine.ext.db import djangoforms
from models import BlogEntry, Profile

class BlogEntryForm(djangoforms.ModelForm):
    class Meta:
        model = BlogEntry
        exclude = ['user']

class ProfileForm(djangoforms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

