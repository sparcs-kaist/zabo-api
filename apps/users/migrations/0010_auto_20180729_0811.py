# Generated by Django 2.0.2 on 2018-07-29 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_zabouser_sid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zabouser',
            name='nickName',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
