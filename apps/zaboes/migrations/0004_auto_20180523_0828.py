# Generated by Django 2.0.2 on 2018-05-23 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zaboes', '0003_auto_20180503_1302'),
    ]

    operations = [
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