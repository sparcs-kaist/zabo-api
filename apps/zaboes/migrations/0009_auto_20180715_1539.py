# Generated by Django 2.0.2 on 2018-07-15 06:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('zaboes', '0008_auto_20180714_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zabo',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 15, 6, 39, 56, 981590, tzinfo=utc)),
        ),
    ]
