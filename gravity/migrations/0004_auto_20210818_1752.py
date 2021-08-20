# Generated by Django 3.1.13 on 2021-08-18 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gravity', '0003_auto_20210811_1800'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inputmodel',
            options={'ordering': ('-publish',)},
        ),
        migrations.AddField(
            model_name='inputmodel',
            name='ID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='data_upload', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inputmodel',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inputmodel',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='inputmodel',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, max_length=250, unique_for_date='publish'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inputmodel',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10),
        ),
        migrations.AddField(
            model_name='inputmodel',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
