# Generated by Django 3.0.6 on 2020-05-26 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20200526_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='uuid',
            field=models.CharField(default='_=\\vbE*uBfVg3|S', max_length=15, unique=True),
        ),
        migrations.DeleteModel(
            name='Verification',
        ),
    ]
