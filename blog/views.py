from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'index.html', context={
                      'title': '我的博客首页', 
                      'welcome': '欢迎访问我的博客首页'
                  })

