import xadmin
from xadmin import views
from .models import Category, Tag, Post
# Register your models here.


class GlobalSetting(object):
    site_title = '博客管理'
    site_footer = '博客管理系统'


class PostAdmin(object):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
    search_fields = ['title', 'category__name']
    style_fields = {'tags': 'm2m_transfer'}
    # style_fields = ['tags']
    # raw_id_fields = ['category']


xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(Category)
xadmin.site.register(Tag)
xadmin.site.register(Post, PostAdmin)
