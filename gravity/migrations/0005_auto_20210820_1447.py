# Generated by Django 3.1.13 on 2021-08-20 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gravity', '0004_auto_20210818_1752'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inputmodel',
            options={},
        ),
        migrations.RemoveField(
            model_name='inputmodel',
            name='ID',
        ),
        migrations.RemoveField(
            model_name='inputmodel',
            name='created',
        ),
        migrations.RemoveField(
            model_name='inputmodel',
            name='publish',
        ),
        migrations.RemoveField(
            model_name='inputmodel',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='inputmodel',
            name='status',
        ),
        migrations.RemoveField(
            model_name='inputmodel',
            name='updated',
        ),
    ]
