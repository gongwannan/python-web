from django.db import models
from tinymce.models import HTMLField
from login.models import User
from mdeditor.fields import MDTextField


# Create your models here.
class Blog(models.Model):
    name = models.CharField(max_length=20, default='Web')

    def __str__(self):
        return self.name


class News(models.Model):
    flclass = (
        ('热点新闻', '热点新闻'),
        ('行业要闻', '行业要闻'),
        ('技术要闻', '技术要闻'),
    )
    wfenlei = (
        ('原创', "原创"),
        ('转载', '转载'),
        ('翻译', '翻译')
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news')
    title = models.CharField(max_length=1000)
    content = HTMLField(max_length=100000)
    contenthead = models.TextField(max_length=100000, default='11')
    p_time = models.DateTimeField(auto_now_add=True)
    fenlei = models.CharField(max_length=128, choices=flclass, default='热点新闻', blank=True)
    blogfenlei = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='sum')
    biaoqian = models.CharField(max_length=128, default='无')
    commend = models.BooleanField(default=False)
    img = models.CharField(blank=True, max_length=100)
    bfenlei = models.CharField(max_length=128, choices=wfenlei, default='转载', blank=True)
    yuedushu = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["p_time"]
        verbose_name = '新闻/博客'
        verbose_name_plural = '新闻/博客'


class Shoucang(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='xihuan')
    blog = models.ForeignKey(News, on_delete=models.CASCADE, related_name='scnumber')

    def __str__(self):
        return self.user.name + '收藏' + self.blog.title

    class Meta:
        verbose_name = '博客收藏'
        verbose_name_plural = '博客收藏'
