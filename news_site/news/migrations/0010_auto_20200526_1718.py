# Generated by Django 3.0.6 on 2020-05-26 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_auto_20200526_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.CharField(default=']_yuLtH@EH@~SvW', max_length=15, unique=True),
        ),
    ]
