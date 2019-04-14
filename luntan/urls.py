#!/user/bin/env/python
# -*- coding:utf-8 -*_
#作者:gongwannan
from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns =[
    path('community/',views.community),
    path('tiezi/<int:id>',views.tiezi),
    path('post/',views.post),
]