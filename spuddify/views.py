# Django and Django app imports
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django import forms
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator, EmailValidator
from spuddify import models

# GAE imports
from google.appengine.ext import db
from google.appengine.api import users

# Misc imports
import re
from datetime import datetime

REGEXES = {'urlsafe':r'^[a-zA-Z0-9_-~ ]*$',
        'article_key':r'[^a-zA-Z0-9_-~]'
        }

# Utility & wrapper functions and objects
class ArticleForm(forms.Form):
    author = forms.CharField(max_length=50)
    title = forms.CharField(max_length=80, 
            validators=[RegexValidator(
                regex=REGEXES['urlsafe'],
                message='Username must be Alphanumeric',
                code='invalid_username'),])
    content = forms.CharField(widget=forms.Textarea)
    status = forms.ChoiceField(choices=models.STATUS_VALUES)

def get_name(value):
     return re.sub(views.REGEXES['article_key'], '', value)

def get_login_context(uri):
    """
    Returns url link and text based on current login status
    """
    if users.get_current_user():
        url = users.create_logout_url(uri)
        url_linktext = 'Logout'
    else:
        url = users.create_login_url(uri)
        url_linktext = 'Login'
    return {'url':url,'url_linktext':url_linktext}

# Main views
def list_articles(request):
    """
    List of all articles in order of edit date
    """ 
    articles = models.Article.all()
    articles.order('-date_edited')
    return render(request, 'list_articles.html', {'articles':articles})

def article_detail(request, article_id):    
    article = models.Article.get(db.Key.from_path('Article', article_id))
    return render(request, 'article_detail.html', {'article':article})

def create_article(request):
    """ 
    If a form has been posted, create a new article or reject it,
    if this is a GET request, return a blank article form.
    """
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article_key = re.sub(REGEXES['article_key'], '', form.cleaned_data['title'])
            article = models.Article(key_name=article_key,
                            title=form.cleaned_data['title'],
                            author=form.cleaned_data['author'],
                            content=form.cleaned_data['content'],
                            status=form.cleaned_data['status'],
                            date_created=datetime.now(),
                            date_edited=datetime.now())
            article.put()
            return HttpResponseRedirect('/articles/' + article_key)
        else:
            return render(request, 'create_article.html', {'form':form})
    else:
        context = get_login_context(reverse(create_article))
        context.update({'form':ArticleForm()})
        return render(request, 'create_article.html', context)

def edit_article(request, article_id):
    """
    Similar to create_article except pre-populate returned form with
    initial values from article instance, and only update article where
    field values have changed.
    """
    article = models.Article.get(db.Key.from_path('Article', article_id))
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            for field in form.cleaned_data:
                if form.cleaned_data[field] != getattr(article, field):
                    setattr(article, field, form.cleaned_data[field])
            article.date_edited = datetime.now()
            article.put()
            return HttpResponseRedirect('/articles/' + article_id)
        else:
            return render(request, 'create_article.html', {'form':form, 'article':article})
    else:
        form = ArticleForm(initial={'author':article.author,
                                    'title':article.title,
                                    'content':article.content,
                                    'status':article.status})
        return render(request, 'edit_article.html', {'form':form, 'article':article})

def delete_article(request, article_id):
    article = models.Article.get(db.Key.from_path('Article', article_id))
    if request.method == 'POST':
        article.delete()
        return redirect(list_articles)
    else:
        return render(request, 'delete_article.html', {'article':article})

def reset(request):
    articles = models.Article.all(keys_only=True)
    db.delete(articles)
    return HttpResponseRedirect('/')