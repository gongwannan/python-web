# Generated by Django 2.1.7 on 2019-05-16 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_remove_user_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateField(default='2019-05-16'),
        ),
    ]
