from django.db import models
from django.forms import ModelForm
from login.models import User
from tinymce.models import HTMLField
import datetime


# Create your models here.


class Luntan(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '论坛类别'
        verbose_name = '论坛类别'


class Fenlei(models.Model):
    name = models.CharField(max_length=20)
    belong = models.ForeignKey(Luntan, on_delete=models.CASCADE, related_name='fenlei')
    jingxuan = models.BooleanField(default=False)

    def __str__(self):
        return self.belong.name + ' ' + self.name

    class Meta:
        verbose_name = '论坛小分支'
        verbose_name_plural = '论坛小分支'


class Tiezi(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tiezi')
    title = models.CharField(max_length=128)
    content = HTMLField(max_length=21845)
    p_time = models.DateTimeField(auto_now_add=True)
    luntan = models.ForeignKey(Fenlei, on_delete=models.CASCADE)
    fangwenshu = models.IntegerField(default=0)
    top = models.BooleanField(default=False)
    mostrecently = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['p_time']
        verbose_name = "帖子"
        verbose_name_plural = "帖子"


class Pinglun(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pinglun')
    tiezi = models.ForeignKey(Tiezi, on_delete=models.CASCADE, related_name="pingluns")
    content = HTMLField(max_length=21845)
    p_time = models.DateTimeField(auto_now_add=True)
    louceng = models.CharField(max_length=10, default=2)

    def __str__(self):
        return self.author.name + '对' + self.tiezi.title + '回复'

    class Meta:
        ordering = ['p_time']
        verbose_name_plural = '评论'
        verbose_name = '评论'


class Relation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="guanzhu")
    luntan = models.ForeignKey(Luntan, on_delete=models.CASCADE, related_name='guanzhushu')

    def __str__(self):
        return self.user.name + '关注' + self.luntan.name

    class Meta:
        verbose_name_plural = '论坛关注关系'
        verbose_name = '论坛关注关系'

class Shoucang(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shoucang")
    tiezi = models.ForeignKey(Tiezi, on_delete=models.CASCADE, related_name='guanzhushu')

    def __str__(self):
        return self.user.name + '关注' + self.tiezi.title

    class Meta:
        verbose_name_plural = '帖子收藏关系'
        verbose_name = '帖子收藏关系'