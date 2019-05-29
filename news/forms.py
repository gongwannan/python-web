from django import forms
from mdeditor.fields import MDTextFormField
from .models import Blog

class blogform(forms.Form):
    fenlei = (
        ('原创', "原创"),
        ('转载', '转载'),
        ('翻译', '翻译')
    )

    bfenlei = forms.ChoiceField(label='文章类型', choices=fenlei)
    blogfenlei = forms.ModelChoiceField(label='博客分类', queryset=Blog.objects.all())