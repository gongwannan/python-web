# Generated by Django 2.1.7 on 2019-06-03 01:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('luntan', '0016_auto_20190603_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tiezi',
            name='mostrecently',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 3, 9, 55, 2, 222270)),
        ),
    ]