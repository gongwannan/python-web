#!/user/bin/env/python
# -*- coding:utf-8 -*_
#作者:gongwannan
from django.urls import path
from . import views

urlpatterns =[
    path('news/', views.news),
    path('new/<int:id>', views.new),

]
