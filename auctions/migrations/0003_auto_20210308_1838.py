# Generated by Django 2.2.12 on 2021-03-08 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20210308_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='actualbid',
            field=models.IntegerField(blank=True),
        ),
    ]
