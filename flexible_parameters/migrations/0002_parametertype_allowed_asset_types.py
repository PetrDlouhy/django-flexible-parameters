# Generated by Django 2.0.2 on 2018-03-19 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0009_assettype_value'),
        ('parameters', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametertype',
            name='allowed_asset_types',
            field=models.ManyToManyField(to='assets.AssetType', verbose_name='Allowed asset types'),
        ),
    ]
