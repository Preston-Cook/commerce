# Generated by Django 4.0.6 on 2022-08-06 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='image_link',
            new_name='image_url',
        ),
    ]
