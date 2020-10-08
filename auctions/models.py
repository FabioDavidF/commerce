from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    starting_bid = models.FloatField()
    img_url = models.URLField(null=True)
    category = models.CharField(max_length=64, null=True)

    def __str__(self):
        return self.title

class Bid(models.Model):
    pass

class Comment(models.Model):
    pass