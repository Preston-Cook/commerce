# Generated by Django 4.0.6 on 2022-08-06 23:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_rename_bid_bid_current_bid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='amount',
            field=models.ForeignKey(default=0.0, on_delete=django.db.models.deletion.CASCADE, to='auctions.bid'),
            preserve_default=False,
        ),
    ]
