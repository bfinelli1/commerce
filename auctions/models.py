from sre_constants import MAX_UNTIL
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class auction_listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img_url = models.URLField(max_length=200)
    category = models.CharField(max_length=64)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name="listing")
    winner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    open = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} ${self.price}"

class comments(models.Model):
    comment = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    listing = models.ForeignKey(auction_listings, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"User: {self.user}, Comment: {self.comment}"

class bids(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    user=models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    listing = models.ForeignKey(auction_listings, on_delete=models.DO_NOTHING)

class watchlists(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    listing = models.ForeignKey(auction_listings, on_delete=models.DO_NOTHING)


#python3 manage.py makemigrations
#python3 manage.py migrate

#python manage.py shell
#from auctions.models import *
#a = auction_listings(title="broom", price=100.99)
#a.save()

#git status
#git add -A
#get reset db.sqlite3
#git commit -m "comment"
#git push -u origin main