from django import template
from spuddify import views
import re

register = template.Library()

@register.filter(name='make_name')
def make_name(value):
    return re.sub(views.REGEXES['article_key'], '', value)