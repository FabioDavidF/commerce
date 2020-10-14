from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True)

class Listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=500)
    bid_quantity = models.IntegerField(default=0)
    starting_bid = models.FloatField(default=0)
    top_bid = models.ForeignKey('Bid', default=0, on_delete=models.SET_DEFAULT)
    img_url = models.URLField(null=True)
    category = models.CharField(max_length=64, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.FloatField()

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)