# Generated by Django 3.1.13 on 2021-12-05 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gravity', '0009_gridtable_sample'),
    ]

    operations = [
        migrations.AddField(
            model_name='gridtable',
            name='k',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='gridtable',
            name='lnA_1',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='gridtable',
            name='lnA_2',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='gridtable',
            name='lnA_3',
            field=models.TextField(null=True),
        ),
    ]
