from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", blank=True, null=True, related_name="watchers")

    def __str__(self):
        return f"{self.username} ({self.email})" 

class Listing(models.Model):
    title = models.CharField(max_length=64)
    category = models.CharField(max_length=64, default="Others")
    seller = models.ForeignKey(User, related_name="user_listings", on_delete=models.CASCADE)
    price = models.ForeignKey("Bid", on_delete=models.CASCADE)
    listing_date = models.DateTimeField(default=timezone.now())
    description = models.TextField()
    image_url = models.URLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}, {self.category}, {self.seller}"

class Bid(models.Model):
    current_bid = models.DecimalField(max_digits=6, decimal_places=2)
    highest_bidder = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    num_bids = models.IntegerField(default=0)

    def __str__(self):
        return f"${self.current_bid:.2f} {self.num_bids} bids"

class Comment(models.Model):
    text = models.TextField()
    time = models.DateTimeField(default=timezone.now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} on {self.listing.title}: {self.text}"





