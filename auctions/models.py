from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass

CHOICES = (
        ('Electronics', 'Electronics'),
        ('Fashion', 'Fashion'),
        ('Toys', 'Toys'),
        ('Home', 'Home'),
        ('Vehicles', 'Vehicles'),
    )


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name="userbid")
    addbid = models.DecimalField(max_digits=6, decimal_places=2)

class Comment(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name="usercomment")
     content = models.CharField(max_length=100)


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name="listing")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    image = models.URLField(max_length=200)
    bids = models.ManyToManyField(Bid, related_name="bids", blank=True)
    starting_price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=300, choices = CHOICES, default='cat')
    comment = models.ManyToManyField(Comment, blank=True, related_name="comments")
    closed = models.BooleanField(default=False)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listings", null=True)