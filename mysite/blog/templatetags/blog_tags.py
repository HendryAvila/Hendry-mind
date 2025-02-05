from django import template
from ..models import Post
from django.db.models import Count
import markdown
from django.utils.safestring import mark_safe
from django.urls import reverse

register = template.Library()
@register.simple_tag()
def total_post():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count = 3):
    latest_posts = Post.published.order_by("-publish")[:count]
    return {'latest_posts':latest_posts}


@register.simple_tag
def get_most_commented_posts(count = 3 ):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return   mark_safe(markdown.markdown(text))


@register.filter('input_type')
def input_type(ob):
    """
    Extract form field type
    :param ob: form field
    :return: string of form field widge type
    """
    return ob.field.widget.__class.__name__

@register.filter('add_classes')
def add_classes(value, arg):
    """
    add provided classes to a form field
    :param value: form field
    :param arg: string of clases separated by ' '
    :return: edited field
    """
    css_classes = value.field.widget.attrs.get('class', '')
    #check if class is set or empty and split its content to list (or init list)
    if css_classes:
        css_classes = css_classes.split(' ')
    else:
        css_classes = []
    #prepare new classes to list
    args = arg.split(' ')
    for a in args:
        if a not in css_classes:
            css_classes.append(a)
    #join back to single string
    return value.as_widget(attrs={'class': ''.join(css_classes)})
