# Generated by Django 4.0.6 on 2022-08-06 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_category_listing_seller_listing_title'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bid',
        ),
        migrations.DeleteModel(
            name='Comments',
        ),
        migrations.DeleteModel(
            name='Listing',
        ),
    ]