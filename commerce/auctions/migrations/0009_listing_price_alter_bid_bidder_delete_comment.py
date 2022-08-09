# Generated by Django 4.0.6 on 2022-08-06 22:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_user_watchlist_comment_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='price',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='auctions.bid'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bid',
            name='bidder',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='offers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
