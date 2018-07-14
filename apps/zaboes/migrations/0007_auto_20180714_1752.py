# Generated by Django 2.0.2 on 2018-07-14 08:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('zaboes', '0006_auto_20180712_0921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zabo',
            name='limit',
        ),
        migrations.AddField(
            model_name='zabo',
            name='url',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='zabo',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 14, 8, 52, 6, 747958, tzinfo=utc)),
        ),
    ]
