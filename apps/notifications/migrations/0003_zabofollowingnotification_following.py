# Generated by Django 2.0.2 on 2018-07-10 16:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0002_auto_20180710_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='zabofollowingnotification',
            name='following',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='notifications_zabofollowingnotification_related_following', related_query_name='notifications_zabofollowingnotifications_following', to=settings.AUTH_USER_MODEL),
        ),
    ]