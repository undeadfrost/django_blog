from django.contrib import admin
from .models import Category, Tag, Post
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
    search_fields = ['title', 'category__name']


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
