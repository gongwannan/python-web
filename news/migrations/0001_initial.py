# Generated by Django 2.1.7 on 2019-05-08 02:38

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('content', tinymce.models.HTMLField(max_length=100000)),
                ('contenthead', models.TextField(default='11', max_length=100000)),
                ('p_time', models.DateTimeField(auto_now_add=True)),
                ('fenlei', models.CharField(choices=[('热点新闻', '热点新闻'), ('行业要闻', '行业要闻'), ('技术要闻', '技术要闻')], default='热点新闻', max_length=128)),
                ('commend', models.BooleanField(default=False)),
                ('img', models.CharField(blank=True, max_length=100)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.User')),
            ],
            options={
                'verbose_name': '新闻',
                'ordering': ['p_time'],
                'verbose_name_plural': '新闻',
            },
        ),
    ]
