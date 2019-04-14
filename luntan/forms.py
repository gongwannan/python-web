#!/user/bin/env/python
# -*- coding:utf-8 -*_
#作者:gongwannan

from django import forms
from tinymce.models import HTMLField

class PinglunForm(forms.Form):
    content = forms.CharField(label='评论', max_length=21845,widget=forms.TextInput)

class TieziForm(forms.Form):
    leibie = (
        ('mobile', '移动开发'),
        ('games', '游戏开发'),
        ('ai', '人工智能'),
    )
    title = forms.CharField(label='标题',max_length=256,widget=forms.TextInput)
    content = forms.CharField(label='内容', max_length=21845, widget=forms.TextInput)
    theme = forms.ChoiceField(label='主题', choices=leibie)


