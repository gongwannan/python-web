from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from django.shortcuts import get_object_or_404
from . import forms
import datetime
from login.models import User


# Create your views here.

def community(request):
    tiezi_list1 = models.Tiezi.objects.order_by('mostrecently')[:5:-1]
    tiezi_list2 = models.Tiezi.objects.order_by('p_time')[:4:-1]
    top = models.Tiezi.objects.filter(top=True).order_by('p_time')[:2:-1]
    tiezi_list3 = models.Tiezi.objects.filter(top=False).order_by('fangwenshu')[:2]
    luntan_list = models.Luntan.objects.order_by('id')
    jingxuan_list = models.Fenlei.objects.filter(jingxuan=True)[:5]
    if request.session['is_login']:
        user = models.User.objects.get(name=request.session['user_name'])
        userid = user.id
        guanzhuluntan_list = user.guanzhu.all()
        guanzhuluntan = []
    else:
        guanzhuluntan = []
        guanzhuluntan_list = []
    for relation in guanzhuluntan_list:
        guanzhuluntan.append(str(relation.luntan.name))

    if request.session['is_login']:
        user = models.User.objects.get(name=request.session['user_name'])
        userid = user.id
        tuijian = guanzhuluntan_list.filter(user_id=userid)
        tuijianluntan = []
        luntanfenzhiid = []
        commend_list = []
        for i in tuijian:
            tuijianluntan.append(i.luntan)
        for luntan in tuijianluntan:
            luntanfenzhi = models.Fenlei.objects.filter(belong=luntan)
            for fenzhi in luntanfenzhi:
                luntanfenzhiid.append(fenzhi.id)
        for i in luntanfenzhiid:
            commend_list += models.Tiezi.objects.filter(luntan_id=i)
            n = commend_list.__len__()

    else:
        commend_list = []
    if request.method == 'POST':
        if request.session['is_login']:
            user = models.User.objects.get(name=request.session['user_name'])
            userid = user.id
            luntanid = request.POST["luntan_id"]
            guanzhu = guanzhuluntan_list.filter(luntan_id=luntanid, user_id=userid)
            if guanzhu.__len__() == 1:
                guanzhu.delete()

                return redirect("/luntan/community/")
            else:
                new_relation = models.Relation()
                new_relation.luntan_id = luntanid
                new_relation.user_id = userid
                new_relation.save()
                return redirect("/luntan/community/")
        else:
            message = '您尚未登录无法使用关注功能'

    return render(request, "luntan/community.html", locals())


def tiezi(request, id):
    tiezi = get_object_or_404(models.Tiezi, pk=id)
    luntan = tiezi.luntan
    pinglun = models.Pinglun.objects.filter(tiezi_id=id)
    pinglun_list = pinglun.order_by('p_time')
    jingxuan_list = models.Fenlei.objects.filter(jingxuan=True)[:5]
    n = len(pinglun_list)
    tiezi.fangwenshu += 1
    tiezi.save()
    if request.session['is_login']:
        user = User.objects.get(name=request.session['user_name'])
        guanzhu_list = user.shoucang.all()
        gaunzhu = []
        for i in guanzhu_list:
            gaunzhu.append(i.tiezi_id)
    else:
        guanzhu = []

    if request.method == 'POST':
        if request.session['is_login']:
            user = User.objects.get(name=request.session['user_name'])
            pinlun_form = forms.PinglunForm(request.POST)
            if pinlun_form.is_valid():
                content = pinlun_form.cleaned_data['content']
                new_pinglun = models.Pinglun()
                new_pinglun.content = content
                new_pinglun.tiezi = tiezi
                new_pinglun.author = User.objects.get(name=request.session['user_name'])
                new_pinglun.p_time = datetime.datetime.now()
                new_pinglun.louceng = n + 2
                new_pinglun.save()
                tiezi.mostrecently = datetime.datetime.now()
                tiezi.save()

                return redirect("/luntan/tiezi/" + str(id))
            else:
                shoucang = models.Shoucang.objects.filter(user_id=user.id, tiezi_id=id)
                if shoucang.__len__() == 1:
                    shoucang.delete()
                    guanzhu_list = user.shoucang.all()
                    gaunzhu = []
                    for i in guanzhu_list:
                        gaunzhu.append(i.tiezi_id)

                    return render(request, "luntan/tiezi.html", locals())
                else:
                    new_relation = models.Shoucang()
                    new_relation.user_id = user.id
                    new_relation.tiezi_id = id
                    new_relation.save()
                    guanzhu_list = user.shoucang.all()
                    gaunzhu = []
                    for i in guanzhu_list:
                        gaunzhu.append(i.tiezi_id)

                    return render(request, "luntan/tiezi.html", locals())



        else:
            message = '您尚未登录无法评论收藏'
    pinlun_form = forms.PinglunForm

    context = {
        'tiezi': tiezi,
        'pinglun_list': pinglun_list,
    }

    return render(request, "luntan/tiezi.html", locals())


def post(request):
    jingxuan_list = models.Fenlei.objects.filter(jingxuan=True)[:5]
    if request.method == 'POST':
        if request.session['is_login']:
            tiezi_form = forms.TieziForm(request.POST)
            if tiezi_form.is_valid():
                title = tiezi_form.cleaned_data['title']
                content = tiezi_form.cleaned_data['content']
                theme = tiezi_form.cleaned_data['luntanfenzhi']
                theme = str(theme)
                theme = theme.split()[1]
                new_tiezi = models.Tiezi()
                new_tiezi.content = content
                new_tiezi.title = title
                new_tiezi.luntan_id = models.Fenlei.objects.get(name=theme).id
                new_tiezi.author = User.objects.get(name=request.session['user_name'])
                new_tiezi.p_time = datetime.datetime.now()
                new_tiezi.mostrecently = datetime.datetime.now()
                new_tiezi.save()

                return redirect("/luntan/community/")
        else:
            message = '您尚未登录无法发帖'

    tiezi_form = forms.TieziForm
    return render(request, 'luntan/post.html', locals())


def luntan(request, id):
    belongname = models.Fenlei.objects.get(id=id).belong.name
    luntanname = models.Fenlei.objects.get(id=id).name
    tiezi_list3 = models.Tiezi.objects.filter(luntan_id=id).order_by('p_time')
    luntan_list = models.Luntan.objects.order_by('id')
    jingxuan_list = models.Fenlei.objects.filter(jingxuan=True)[:5]
    if request.session['is_login']:
        user = models.User.objects.get(name=request.session['user_name'])
        userid = user.id
        guanzhuluntan_list = user.guanzhu.all()
        guanzhuluntan = []
    else:
        guanzhuluntan = []
        guanzhuluntan_list = []
    for relation in guanzhuluntan_list:
        guanzhuluntan.append(str(relation.luntan.name))
    top = models.Tiezi.objects.filter(top=True).order_by('p_time')
    if request.session['is_login']:
        user = models.User.objects.get(name=request.session['user_name'])
        userid = user.id
        tuijian = guanzhuluntan_list.filter(user_id=userid)
        tuijianluntan = []
        luntanfenzhiid = []
        commend_list = []
        for i in tuijian:
            tuijianluntan.append(i.luntan)
        for luntan in tuijianluntan:
            luntanfenzhi = models.Fenlei.objects.filter(belong=luntan)
            for fenzhi in luntanfenzhi:
                luntanfenzhiid.append(fenzhi.id)
        for i in luntanfenzhiid:
            commend_list += models.Tiezi.objects.filter(luntan_id=i)
    else:
        commend_list = []
    if request.method == 'POST':
        if request.session['is_login']:
            user = models.User.objects.get(name=request.session['user_name'])
            userid = user.id
            luntanid = request.POST["luntan_id"]
            guanzhu = guanzhuluntan_list.filter(luntan_id=luntanid, user_id=userid)
            if guanzhu.__len__() == 1:
                guanzhu.delete()

                return render(request, 'luntan/lutan.html', locals())
            else:
                new_relation = models.Relation()
                new_relation.luntan_id = luntanid
                new_relation.user_id = userid
                new_relation.save()
                return render(request, 'luntan/lutan.html', locals())
        else:
            message = '您尚未登录无法使用关注功能'

    return render(request, 'luntan/lutan.html', locals())
