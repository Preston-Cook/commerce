# Generated by Django 4.0.6 on 2022-08-07 00:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_alter_listing_listing_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(null=True, related_name='watchers', to='auctions.listing'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='listing_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 7, 0, 52, 7, 147049, tzinfo=utc)),
        ),
    ]