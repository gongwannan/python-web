from django.shortcuts import render, redirect
from . import models
from django.shortcuts import get_object_or_404
from . import forms
from login.models import User
import datetime
from login.models import Follow


# Create your views here.

def news(request):
    news_list1 = models.News.objects.order_by('p_time')[:10]
    news_list2 = models.News.objects.order_by('p_time')[10:20]
    news_list3 = models.News.objects.order_by('p_time')[20:30]
    news_list4 = models.News.objects.order_by('p_time')[30:40]
    blog_list = models.Blog.objects.all()

    commend_list = models.News.objects.filter(commend=True).order_by('p_time')[:5:-1]
    return render(request, 'news/news.html', locals())


def new(request, id):
    new = get_object_or_404(models.News, pk=id)
    authorid = new.author_id

    new.yuedushu += 1
    new.save()
    if request.method == 'POST':
        if request.session['is_login']:
            user = User.objects.get(name=request.session['user_name'])
            userid = user.id
            authorid = request.POST["author_id"]
            guanzhu = Follow.objects.filter(follow_id=authorid, user_id=userid)
            if guanzhu.__len__() == 1:
                guanzhu.delete()
                guanzhu_list = user.follows.all()
                gaunzhu = []
                for i in guanzhu_list:
                    gaunzhu.append(str(i.follow.name))
                return render(request, "news/new.html", locals())
            else:
                new_relation = Follow()
                new_relation.follow_id = authorid
                new_relation.user_id = userid
                new_relation.save()
                guanzhu_list = user.follows.all()
                gaunzhu = []
                for i in guanzhu_list:
                    gaunzhu.append(str(i.follow.name))
                return render(request, "news/new.html", locals())
        else:
            message = '您尚未登录无法使用关注功能'
    if request.session['is_login']:
        user = User.objects.get(name=request.session['user_name'])
        userid = user.id
        guanzhu_list = user.follows.all()
        gaunzhu = []
    else:
        gaunzhu = []
        guanzhu_list = []
    for i in guanzhu_list:
        gaunzhu.append(str(i.follow.name))
    return render(request, "news/new.html", locals())


def hynews(request):
    news_list1 = models.News.objects.filter(fenlei='行业要闻')
    commend_list = models.News.objects.filter(commend=True).order_by('p_time')[:5]
    return render(request, "news/hynews.html", locals())


def rdnews(request):
    news_list1 = models.News.objects.filter(fenlei='热点新闻')
    commend_list = models.News.objects.filter(commend=True).order_by('p_time')[:5]
    return render(request, "news/rdnews.html", locals())


def jsnews(request):
    news_list1 = models.News.objects.filter(fenlei='技术要闻')
    commend_list = models.News.objects.filter(commend=True).order_by('p_time')[:5]
    return render(request, 'news/jsnews.html', locals())


def boke(request):
    if request.session['is_login']:
        blogform = forms.blogform(request.POST)
        if blogform.is_valid():
            bfenlei = blogform.cleaned_data['bfenlei']
            blogfenlei = blogform.cleaned_data['blogfenlei']
            content = request.POST['content']
            biaoqian = request.POST['biaoqian']
            title = request.POST['title']
            blog = models.News()
            blog.title = title
            blog.author = User.objects.get(name=request.session['user_name'])
            blog.content = content
            blog.biaoqian = biaoqian
            blog.blogfenlei = models.Blog.objects.get(name=blogfenlei)
            blog.p_time = datetime.datetime.now()
            blog.bfenlei = bfenlei
            blog.commend = False
            blog.contenthead = request.POST['contenthead']
            blog.save()
            message = '发表成功!'
            return render(request, 'news/xieboke.html', locals())

    else:
        message = '您尚未登录无法发表博客'
    blogform = forms.blogform()
    return render(request, 'news/xieboke.html', locals())


def upload_img(request):
    pass

def blog(request):
    user = user = User.objects.get(name=request.session['user_name'])
    blog_list = models.News.objects.filter(author=user)
    return render(request, 'news/blog.html', locals())

def blogmk(request, id):
    blogmk_list = models.Blog.objects.all()
    blogmk = get_object_or_404(models.Blog, pk=id)
    blog_list = models.News.objects.filter(blogfenlei_id=id)
    return render(request, 'news/blogmk.html', locals())