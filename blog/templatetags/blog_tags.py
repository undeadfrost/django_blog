from ..models import Post, Category
from django import template
from django.db.models.aggregates import Count


register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all()[:num]


@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gte=1)
