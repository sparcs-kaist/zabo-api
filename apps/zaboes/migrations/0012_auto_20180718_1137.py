# Generated by Django 2.0.2 on 2018-07-18 11:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('zaboes', '0011_auto_20180715_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zabo',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='zabo',
            name='deadline',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]