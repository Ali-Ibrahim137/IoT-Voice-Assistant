# Generated by Django 2.1 on 2019-03-18 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vinus', '0015_merge_20190315_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='thinger_api',
            name='type',
            field=models.IntegerField(choices=[(1, 'Output Resources'), (2, 'Input Resources'), (3, 'Input/Output Resources'), (4, 'Resources without parameters')], default=1),
        ),
        migrations.AlterField(
            model_name='resources',
            name='type',
            field=models.IntegerField(choices=[(1, 'Output Resources'), (2, 'Input Resources')], default=1),
        ),
    ]
