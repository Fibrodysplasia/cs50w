from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    return render(request, "auctions/listing.html", {
        "title": listing.title,
        "description": listing.description,
        "start_bid": listing.start_bid,
        "current_bid": listing.current_bid,
        "buy_now": listing.buy_now,
        "bids": Bid.objects.filter(listing=listing),
        "end_date": listing.end_date,
        "image_link": listing.image_link,
        "seller": listing.seller,
        "comments": Comment.objects.filter(listing=listing),
        "watched_by": listing.watched_by.all(),
        "listing_id": listing_id,
    })

def new_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        start_bid = request.POST["start_bid"]
        buy_now = request.POST["buy_now"]
        end_date = request.POST["end_date"]
        image_link = request.POST["image_link"]
        seller = request.user
        listing = Listing(title=title, description=description, start_bid=start_bid, buy_now=buy_now, end_date=end_date, image_link=image_link, seller=seller)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/new_listing.html")
    
def bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        amount = int(request.POST["amount"])
        bidder = request.user
        current = int(listing.current_bid.amount)
        buyout = int(listing.buy_now.amount)
        bid = Bid(amount=amount, bidder=bidder, listing=listing)
        # wallet -= amount
        if amount > current and amount < buyout:
            bid.save()
            listing.current_bid = amount
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        elif amount == buyout:
            bid.save()
            listing.current_bid = amount
            listing.title = "SOLD: {{ listing.title }}"
        elif amount > buyout:
            return render(request, "auctions/listing.html", {
                "message": "You cannot bid more than the buy now price."
            })
        else:
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        return render(request, "auctions/bid.html", {
            "listing": listing,
        })
        
def comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        content = request.POST["comment"]
        user = request.user
        comment = Comment(content=content, user=user, listing_id=listing_id)
        comment.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        
        