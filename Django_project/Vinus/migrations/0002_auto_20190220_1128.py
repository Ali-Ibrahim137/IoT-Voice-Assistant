# Generated by Django 2.1.4 on 2019-02-20 11:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Vinus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='user',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='resources',
            name='thinger_api',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='Vinus.THINGER_API'),
        ),
        migrations.AddField(
            model_name='thinger_api',
            name='device',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='Vinus.Device'),
        ),
    ]
