# Generated by Django 2.1.7 on 2019-06-03 01:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('luntan', '0015_auto_20190603_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tiezi',
            name='mostrecently',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 3, 9, 50, 46, 424838)),
        ),
    ]
