# Generated by Django 2.0.2 on 2018-03-19 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parameters', '0002_parametertype_allowed_asset_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='value',
            field=models.SlugField(max_length=255, verbose_name='value'),
        ),
    ]
