from google.appengine.ext import db
from google.appengine.api import users
from datetime import datetime

STATUS_VALUES = [('dra', 'Draft'), ('pub', 'Published'), ('del', 'Deleted')]

class Author(db.Model):
    name = db.StringProperty()
    
class Content(db.Model):
    """ Abstract class for user content """
    
    data = db.TextProperty()
    createdAt = db.DateTimeProperty()
    
class Article(db.Model):
    """ Blog article, content with title, status """
    
    author = db.StringProperty()
    title = db.StringProperty()
    content = db.TextProperty()
    status = db.StringProperty(choices=[status[0] for status in STATUS_VALUES])
    date_created = db.DateTimeProperty()
    date_edited = db.DateTimeProperty()

class Comment(Content, db.Model):
    """ Article comment. Must reference an article """
    
    article = db.ReferenceProperty(Article, collection_name='comments')
    content = db.TextProperty()