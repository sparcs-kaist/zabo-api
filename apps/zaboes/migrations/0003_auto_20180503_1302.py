# Generated by Django 2.0.2 on 2018-05-03 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zaboes', '0002_auto_20180502_1028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poster',
            name='order',
        ),
        migrations.RemoveField(
            model_name='zabo',
            name='posters_num',
        ),
        migrations.AlterField(
            model_name='comment',
            name='zabo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='zaboes.Zabo'),
        ),
        migrations.AlterField(
            model_name='poster',
            name='zabo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posters', to='zaboes.Zabo'),
        ),
        migrations.AlterField(
            model_name='recomment',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recomments', to='zaboes.Comment'),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='zabo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timeslots', to='zaboes.Zabo'),
        ),
    ]
