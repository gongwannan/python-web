from django import forms
from captcha.fields import CaptchaField
from django.contrib.admin import widgets


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label="验证码")


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=259,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')


class TouxiangForm(forms.Form):
    touxiang = forms.ImageField(label='头像')


class UsermessageForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    name = forms.CharField(label='昵称', max_length=20, widget=forms.TextInput())
    truename = forms.CharField(label='实名', max_length=20, widget=forms.TextInput())
    birthday = forms.DateField(label='生日', widget=widgets.AdminDateWidget())
    diqu = forms.CharField(label='地区', max_length=40, widget=forms.TextInput())
    sex = forms.ChoiceField(label='性别', choices=gender)
    jianjie = forms.CharField(label='简介', max_length=1000, widget=forms.Textarea())
