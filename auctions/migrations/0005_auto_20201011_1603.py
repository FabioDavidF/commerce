# Generated by Django 3.1.1 on 2020-10-11 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20201011_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='top_bid',
            field=models.FloatField(default=0),
        ),
    ]