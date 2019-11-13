#!/user/bin/env/python
# -*- coding:utf-8 -*_
# 作者:gongwannan
from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.news),
    path('new/<int:id>', views.new),
    path('firenews/', views.rdnews),
    path('hangyenews/', views.hynews),
    path('jishunews/', views.jsnews),
    path('boke/', views.boke),
    path('upload_img/', views.upload_img, name='upload_img'),
    path('blog/', views.blog),
    path('blogmk/<int:id>', views.blogmk),
]
app_name = 'news'
