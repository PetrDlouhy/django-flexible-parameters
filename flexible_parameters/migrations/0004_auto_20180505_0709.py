# Generated by Django 2.0.2 on 2018-05-05 05:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0011_auto_20180319_1629'),
        ('parameters', '0003_auto_20180319_1629'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='baseparameter',
            unique_together={('parameter_type', 'asset')},
        ),
    ]
