# Generated by Django 2.0.2 on 2018-07-11 07:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('zaboes', '0003_auto_20180711_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zabo',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 11, 7, 43, 8, 761841, tzinfo=utc)),
        ),
    ]
