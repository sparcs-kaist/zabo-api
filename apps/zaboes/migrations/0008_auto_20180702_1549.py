# Generated by Django 2.0.2 on 2018-07-02 15:49

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('zaboes', '0007_remove_zabo_like_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='user',
            new_name='zaboUser',
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('zabo', 'zaboUser')},
        ),
    ]
