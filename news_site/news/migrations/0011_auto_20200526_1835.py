# Generated by Django 3.0.6 on 2020-05-26 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_auto_20200526_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.CharField(default='b^yWS=82o.:*85m', max_length=15, unique=True),
        ),
    ]
