# Generated by Django 3.0.6 on 2020-05-26 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_auto_20200526_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.CharField(default=',):!n4LrE%;;y0\\', max_length=15, unique=True),
        ),
    ]
