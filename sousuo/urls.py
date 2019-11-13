from django.urls import path
from . import views

urlpatterns = [
    path('sousuo/', views.sousuo),
    path('news/', views.news),
    path('tiezi/', views.tiezi),
    path('yonghu/', views.user),
    path('newsfw/', views.newsfw),
]