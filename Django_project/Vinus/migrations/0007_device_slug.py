# Generated by Django 2.1.4 on 2019-02-27 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vinus', '0006_auto_20190223_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='slug',
            field=models.SlugField(default=True),
        ),
    ]
