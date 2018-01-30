from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Post, Category, Tag
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
import markdown


# Create your views here.
def get_pagination_data(paginator, page_obj, is_paginated):
    if is_paginated:
        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        page_number = page_obj.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range
        if page_number == 1:
            right = page_range[page_number: page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0: page_number - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0: page_number - 1]
            right = page_range[page_number: page_number + 2]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages:
                last = True
            if right[-1] < total_pages - 1:
                right_has_more = True
        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last
        }
        return data
    else:
        return {}


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = get_pagination_data(paginator, page_obj, is_paginated)
        context.update(pagination_data)
        return context

    # def get_pagination_data(self, paginator, page_obj, is_paginated):
    #     if is_paginated:
    #         left = []
    #         right = []
    #         left_has_more = False
    #         right_has_more = False
    #         first = False
    #         last = False
    #         page_number = page_obj.number
    #         total_pages = paginator.num_pages
    #         page_range = paginator.page_range
    #         if page_number == 1:
    #             right = page_range[page_number: page_number+2]
    #             if right[-1] < total_pages-1:
    #                 right_has_more = True
    #             if right[-1] < total_pages:
    #                 last = True
    #         elif page_number == total_pages:
    #             left = page_range[(page_number-3) if (page_number-3) > 0 else 0: page_number-1]
    #             if left[0] > 2:
    #                 left_has_more = True
    #             if left[0] > 1:
    #                 first = True
    #         else:
    #             left = page_range[(page_number-3) if (page_number-3) > 0 else 0: page_number-1]
    #             right = page_range[page_number: page_number+2]
    #             if left[0] > 2:
    #                 left_has_more = True
    #             if left[0] > 1:
    #                 first = True
    #             if right[-1] < total_pages:
    #                 last = True
    #             if right[-1] < total_pages - 1:
    #                 right_has_more = True
    #         data = {
    #             'left': left,
    #             'right': right,
    #             'left_has_more': left_has_more,
    #             'right_has_more': right_has_more,
    #             'first': first,
    #             'last': last
    #         }
    #         return data
    #     else:
    #         return {}


class InfoView(DetailView):
    model = Post
    template_name = 'blog/info.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(InfoView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super(InfoView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        context = super(InfoView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArchivesView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = get_pagination_data(paginator, page_obj, is_paginated)
        context.update(pagination_data)
        return context

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return Post.objects.filter(
            created_time__year=year,
            created_time__month=month
        )


class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = get_pagination_data(paginator, page_obj, is_paginated)
        context.update(pagination_data)
        return context

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return Post.objects.filter(category=cate)


class TagView(ListView):
    model = Tag
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = get_pagination_data(paginator, page_obj, is_paginated)
        context.update(pagination_data)
        return context

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return Post.objects.filter(tags=tag)


def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = '请输出搜索内容'
        return render(request, 'blog/index.html', {'error_msg': error_msg})
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'post_list': post_list})
