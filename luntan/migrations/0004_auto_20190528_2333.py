# Generated by Django 2.1.7 on 2019-05-28 15:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('luntan', '0003_auto_20190518_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tiezi',
            name='mostrecently',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 28, 23, 33, 4, 793268)),
        ),
    ]