import datetime
import hashlib
import pytz
from django.conf import settings
from django.shortcuts import render, redirect
from . import models
from . import forms
from login import my_utils
import os
from luntan.models import Tiezi,Pinglun
from news.models import News


# Create your views here.


def login(request):
    if request.session.get('is_login', None):
        return redirect("/news/news/")
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if not user.has_confirmed:
                    message = "该用户还未通过邮件确认！"
                    return render(request, 'login/login.html', locals())
                if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['touxiang'] = str(user.touxiang)
                    return redirect('/news/news/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)  # 使用加密密码
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email, code)

                message = '请前往注册邮箱，进行邮件确认！'
                return render(request, 'login/confirm.html', locals())  # 跳转到等待邮件确认页面。
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/news/news/')
    request.session.flush()
    request.session['is_login'] = False

    return redirect("/news/news/")


def hash_code(s, salt='mysite'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def test(request):
    return render(request, 'login/test.html')


def huanying(request):
    return render(request, 'login/huanying.html')


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user, )
    return code


def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '来自极客交流社区的注册确认邮件'

    text_content = '''感谢注册，这里是极客交流社区站点，专注于技术的分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/login/confirm/?code={}" target=blank>www.jike.com</a>，\
                    这里极客交流社区站点，专注于技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    now = now.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())


def usermessage(request):
    name = request.session['user_name']
    user = models.User.objects.get(name=name)
    if request.method == 'POST':
        usermessage_form = forms.UsermessageForm(request.POST)
        if usermessage_form.is_valid():
            username = usermessage_form.cleaned_data['name']
            truename = usermessage_form.cleaned_data['truename']
            birthday = usermessage_form.cleaned_data['birthday']
            diqu = usermessage_form.cleaned_data['diqu']
            sex = usermessage_form.cleaned_data['sex']
            jianjie = usermessage_form.cleaned_data['jianjie']
            user.name = username
            user.truename = truename
            user.sex = sex
            user.birthday = birthday
            user.jianjie = jianjie
            user.diqu = diqu
            user.save()
            return render(request, 'login/usermessage.html', locals())
        else:
            touxiang = request.FILES['touxiang']
            # 拿文件数据
            # 获取图片的随机名
            file_name = 'images/' + my_utils.utils.get_random_str() + '.jpg'
            # 拼接一个自己的文件路径
            image_path = os.path.join(settings.MEDIA_ROOT, file_name)
            # 打开拼接的文件路径
            with open(image_path, 'wb')as fp:
                # 遍历图片的块数据（切块的传图片）
                for i in touxiang.chunks():
                    # 将图片数据写入自己的那个文件
                    fp.write(i)
            # 拼接返回数据
            user.touxiang = file_name
            user.save()
            return render(request, 'login/usermessage.html', locals())
    touxiang_form = forms.TouxiangForm()
    xinxi_form = forms.UsermessageForm()
    return render(request, 'login/usermessage.html', locals())

def about(request):
    pass
    return render(request, 'login/about.html', locals())


def geren(request):
    name = request.session['user_name']
    user = models.User.objects.get(name=name)
    tiezi_list = Tiezi.objects.filter(author=user)
    news_list = News.objects.filter(author=user)
    pinglun_list = Pinglun.objects.filter(author=user)

    return render(request, 'login/geren.html', locals())

def shoucang(request):
    name = request.session['user_name']
    user = models.User.objects.get(name=name)
    news_list = user.xihuan.all()
    tiezi_list = user.shoucang.all()
    return render(request, 'login/shoucang.html', locals())

def guanzhu(request):
    name = request.session['user_name']
    user = models.User.objects.get(name=name)
    guanzhu_list = user.follows.all()
    return render(request, 'login/guanzhu.html', locals())

def fensi(request):
    name = request.session['user_name']
    user = models.User.objects.get(name=name)
    fensi_list = user.fans.all()
    return render(request, 'login/fensi.html', locals())

def zhanghao(request):
    pass
    return render(request, 'login/zhanghao.html', locals())

def mima(request):
    pass
    return render(request, 'login/mima.html', locals())

def youxiang(request):
    pass
    return render(request, 'login/youxiang.html', locals())