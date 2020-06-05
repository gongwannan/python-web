# Generated by Django 2.1.7 on 2019-05-29 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='bfenlei',
            field=models.CharField(blank=True, choices=[('原创', '原创'), ('转载', '转载'), ('翻译', '翻译')], default='转载', max_length=128),
        ),
    ]