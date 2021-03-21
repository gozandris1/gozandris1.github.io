from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

class Category(models.Model):
    categoryName = models.CharField(max_length=64)

    def __str__(self):
        return f"({self.id}) {self.categoryName}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=256)
    startingbid = models.IntegerField()
    actualbid = models.IntegerField(null=True)
    picture = models.CharField(max_length=256)
    categorytype = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctionItems")
#    watchers = models.ManyToManyField(User, blank=True, related_name="watchItems")
#    number_of_bids = models.IntegerField(blank=True)
#    time_starting = models.DateTimeField(blank=True)
#    time_ending = models.DateTimeField(blank=True)

    def __str__(self):
        return f"{self.categorytype} - {self.title}"

class Watchlist(models.Model):
       user_id = models.ForeignKey(User, on_delete=models.CASCADE)
       listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Bid(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_time = models.DateTimeField()

class Comments(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    time_sent = models.DateTimeField(blank=True)