from django.contrib.auth.models import AbstractUser
from django.db import models
from djmoney.models.fields import MoneyField


class User(AbstractUser):
    # inheriting from AbstractUser gives
    # username, email, password
    wallet_balance = MoneyField(max_digits=19, decimal_places=2, null=True, default_currency='USD')
    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    start_bid = MoneyField(max_digits=19, decimal_places=2, null=True, default_currency='USD')
    buy_now = MoneyField(max_digits=19, decimal_places=2, null=True, default_currency='USD')
    current_bid = MoneyField(max_digits=19, decimal_places=2, null=True, default_currency='USD')
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leader', null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sold_by')
    end_date = models.DateTimeField()
    image_link = models.CharField(max_length=256)
    watched_by = models.ManyToManyField(User, blank=True, related_name="watching")
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='won_by')
    def __str__(self):
        return f"Listing: {self.title}"
    
class Category(models.Model):
    name = models.CharField(max_length=64)
    listings = models.ManyToManyField(Listing, blank=True)
    def __str__(self):
        return f"Category: {self.name}"
    
class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    def __str__(self):
        return f"User: {self.user} Comment: {self.content}"
    
class Bid(models.Model):
    amount = MoneyField(max_digits=19, decimal_places=2, null=True, default_currency='USD')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    def __str__(self):
        return f"Bidder: {self.bidder} Bid: {self.amount}"
