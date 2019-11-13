from django.shortcuts import render, redirect
from . import models
from login.models import User
from luntan.models import Tiezi
from news.models import News


# Create your views here.
def sousuo(request):
    if request.method == "POST":
        content = request.POST["content"]
        if len(content) == 0:
            return render(request, 'sousuo/logo.html', locals())
        else:
            news_list = News.objects.filter(content__icontains=content)
            tiezi_list = Tiezi.objects.filter(title__icontains=content)
            user_list = User.objects.filter(name__icontains=content)
            request.session['content'] = content
            return render(request, 'sousuo/sousuo.html', locals())
    return render(request, 'sousuo/sousuo.html', locals())


def news(request):
    content = request.session['content']
    news_list = News.objects.filter(content__icontains=content)

    if request.method == "POST":
        content = request.POST["content"]
        news_list = News.objects.filter(content__icontains=content)
        request.session['content'] = content
        return render(request, 'sousuo/news.html', locals())
    return render(request, 'sousuo/news.html', locals())


def tiezi(request):
    content = request.session['content']
    tiezi_list = Tiezi.objects.filter(title__icontains=content)
    if request.method == "POST":
        content = request.POST["content"]
        tiezi_list = Tiezi.objects.filter(title__icontains=content)
        request.session['content'] = content
        return render(request, 'sousuo/tiezi.html', locals())
    return render(request, 'sousuo/tiezi.html', locals())


def user(request):
    content = request.session['content']
    user_list = User.objects.filter(name__icontains=content)
    if request.method == "POST":
        content = request.POST["content"]
        user_list = User.objects.filter(name__icontains=content)
        request.session['content'] = content
        return render(request, 'sousuo/user.html', locals())
    return render(request, 'sousuo/user.html', locals())


def newsfw(request):
    content = request.session['content']
    news_list = News.objects.filter(content__icontains=content).order_by('yuedushu')

    if request.method == "POST":
        content = request.POST["content"]
        news_list = News.objects.filter(content__icontains=content)
        request.session['content'] = content
        return render(request, 'sousuo/news.html', locals())
    return render(request, 'sousuo/news.html', locals())
