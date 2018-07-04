# Generated by Django 2.0.2 on 2018-06-28 08:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('zaboes', '0003_auto_20180503_1302'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('zabo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='zaboes.Zabo')),
            ],
        ),
        migrations.RemoveField(
            model_name='timeslot',
            name='is_main',
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='recomment',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='content',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='end_time',
            field=models.DateTimeField(default=None),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='start_time',
            field=models.DateTimeField(default=None),
        ),
        migrations.AlterField(
            model_name='poster',
            name='image',
            field=models.FileField(upload_to='posters/'),
        ),
        migrations.AlterField(
            model_name='poster',
            name='zabo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posters', to='zaboes.Zabo'),
        ),
    ]
