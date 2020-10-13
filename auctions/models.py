from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True)

class Listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=512, default='No description')
    bid_quantity = models.IntegerField(default=0)
    if bid_quantity == 0:
        top_bid = models.FloatField(default=0)
    elif bid_quantity > 0:
        top_bid = models.ForeignKey('Bid')
    img_url = models.URLField(null=True)
    category = models.CharField(max_length=64, null=True)

    def __str__(self):
        return self.title

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.FloatField()

class Comment(models.Model):
    pass