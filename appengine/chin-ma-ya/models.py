# -*- encoding: utf-8 -*-

from google.appengine.ext import db

class Area(db.Model):
    id = db.IntegerProperty(required=True)
    name = db.StringProperty(verbose_name='地域名', required=True)
    url = db.LinkProperty(verbose_name='URL', required=True)
    updated_at = db.DateTimeProperty(verbose_name='更新日時', required=True, auto_now=True)
    created_at = db.DateTimeProperty(verbose_name='作成日時', required=True, auto_now_add=True)

class Shop(db.Model):
    id = db.IntegerProperty(required=True)
    area = db.ReferenceProperty(Area, verbose_name='地域', required=True)
    name = db.StringProperty(verbose_name='店舗名', required=True)
    address = db.StringProperty(verbose_name='住所', required=True)
    geo = db.GeoPtProperty(verbose_name='経度緯度', required=True)
    extra = db.TextProperty(verbose_name='追加情報')
    updated_at = db.DateTimeProperty(verbose_name='更新日時', auto_now=True, required=True)
    created_at = db.DateTimeProperty(verbose_name='作成日時', auto_now_add=True, required=True)

class BlogEntry(db.Model):
    user = db.UserProperty(verbose_name='ユーザー', required=True)
    shop = db.ReferenceProperty(verbose_name='店舗', required=True)
    title = db.StringProperty(verbose_name='タイトル', required=True)
    body = db.TextProperty(verbose_name='本文', required=True)
    updated_at = db.DateTimeProperty(verbose_name='更新日時', auto_now=True, required=True)
    created_at = db.DateTimeProperty(verbose_name='作成日時', auto_now_add=True, required=True)

class Photo(db.Model):
    user = db.UserProperty(verbose_name='ユーザー', required=True)
    shop = db.ReferenceProperty(verbose_name='店舗')
    title = db.StringProperty(verbose_name='タイトル', required=True)
    image = db.BlobProperty(verbose_name='画像', required=True)
    mime_type = db.StringProperty(verbose_name='MIMEタイプ', required=True)
    filename = db.StringProperty(verbose_name='ファイル名', required=True)
    size = db.IntegerProperty(verbose_name='ファイルサイズ', required=True)
    updated_at = db.DateTimeProperty(verbose_name='更新日時', auto_now=True, required=True)
    created_at = db.DateTimeProperty(verbose_name='作成日時', auto_now_add=True, required=True)

class Profile(db.Model):
    user = db.UserProperty(verbose_name='ユーザー', required=True)
    username = db.StringProperty(verbose_name='ユーザー名', required=True)
    updated_at = db.DateTimeProperty(verbose_name='更新日時', auto_now=True, required=True)
    created_at = db.DateTimeProperty(verbose_name='作成日時', auto_now_add=True, required=True)

