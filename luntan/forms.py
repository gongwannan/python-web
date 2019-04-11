#!/user/bin/env/python
# -*- coding:utf-8 -*_
#作者:gongwannan

from django import forms
from tinymce.models import HTMLField

class PinglunForm(forms.Form):
    content = forms.CharField(label='评论', max_length=21845,widget=forms.TextInput)



