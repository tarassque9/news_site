# Generated by Django 3.0.6 on 2020-06-09 10:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0014_auto_20200608_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moderationpost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 9, 13, 31, 32, 272116)),
        ),
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.CharField(default='8b7cb065fbb5418ba99809f8e18e52a2', max_length=40, unique=True),
        ),
    ]