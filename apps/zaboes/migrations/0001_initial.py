# Generated by Django 2.0.2 on 2018-04-04 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=140)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('is_private', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_blocked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Participate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('participants', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='posters/%Y/%m/%d/')),
            ],
        ),
        migrations.CreateModel(
            name='Recomment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=140)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('is_private', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_blocked', models.BooleanField(default=False)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zaboes.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Timeslot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_main', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Zabo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=50)),
                ('content', models.TextField(blank=True, null=True)),
                ('category', models.CharField(choices=[('R', 'Recruting'), ('P', 'Performance'), ('C', 'Competition'), ('F', 'Fair'), ('L', 'Lecture'), ('E', 'Exhibition')], max_length=1)),
                ('apply', models.CharField(choices=[('Z', 'Apply by zabo'), ('S', 'On-site reception'), ('E', 'External application')], max_length=1)),
                ('payment', models.CharField(choices=[('F', 'FREE'), ('Z', 'Paid by zabo'), ('A', 'Payment on account')], max_length=1)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('limit', models.IntegerField(default=1000)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_validated', models.BooleanField(default=False)),
                ('founder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='timeslot',
            name='zabo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zaboes.Zabo'),
        ),
        migrations.AddField(
            model_name='poster',
            name='zabo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zaboes.Zabo'),
        ),
        migrations.AddField(
            model_name='participate',
            name='zabo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zaboes.Zabo'),
        ),
        migrations.AddField(
            model_name='comment',
            name='zabo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zaboes.Zabo'),
        ),
    ]
