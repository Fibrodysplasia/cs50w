from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

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
    categories = Category.objects.filter(listings=listing)
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
        
        # there has to be a better way to do this
        "comments": reversed(Comment.objects.filter(listing=listing_id)[::-1][:3]),
        "watched_by": listing.watched_by.all(),
        "categories": categories,
        "listing_id": listing_id,
        "is_active": listing.is_active,
    })

# Default url for login_required is "/accounts/login/"
# this can be changed in settings.py
@login_required
def new_listing(request):
    # I could use a form with class Meta: model=Listing
    # and then choose fields, but I didn't think about it
    # until after I had finished this portion of the project.
    # In hindsight, it would probably display the MoneyField
    # in a more user-friendly way.
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        start_bid = request.POST["start_bid"]
        buy_now = request.POST["buy_now"]
        end_date = request.POST["end_date"]
        image_link = request.POST["image_link"]
        seller = request.user
        listing = Listing(title=title, description=description, start_bid=start_bid, current_bid=start_bid, buy_now=buy_now, end_date=end_date, image_link=image_link, seller=seller)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/new_listing.html")
    
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })
    
def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": Listing.objects.filter(category=category)
    })
    
@login_required
def new_category(request):
    if request.method == "POST":
        name = request.POST["name"]
        category = Category(name=name)
        category.save()
        return HttpResponseRedirect(reverse("categories"))
    else:
        return render(request, "auctions/categories.html")
    
@login_required
def add_to_category(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        name = request.POST["category"]
        if Category.objects.filter(name=name).exists():
            category = Category.objects.get(name=name)
            category.listings.add(listing)
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        else:
            name = request.POST["category"]
            category = Category(name=name)
            category.save()
            category.listings.add(listing)
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def remove_from_category(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    category = Category.objects.get(pk=request.POST["category_id"])
    if request.method == "POST":
        category.listings.remove(listing)
        return HttpResponseRedirect(reverse("category", args=(category.id,)))

@login_required
def bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST" and listing.is_active:
        amount = int(request.POST["amount"])
        bidder = request.user
        current = int(listing.current_bid.amount)
        buyout = int(listing.buy_now.amount)
        bid = Bid(amount=amount, bidder=bidder, listing=listing)
        # wallet -= amount
        if amount <= current:
            messages.error(request, "Bid must be greater than current bid.")
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        elif amount > buyout:
            messages.error(request, "Bid cannot be higher than buy now price.")
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        elif amount == buyout:
            bid.save()
            listing.current_bid = amount
            listing.watched_by.add(bidder)
            listing.is_active = False
            listing.save()
            messages.success(request, "You have won the auction!")
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        elif amount > current and amount < buyout:
            bid.save()
            listing.current_bid = amount
            listing.save()
            listing.watched_by.add(bidder)
            messages.success(request, "Bid successful!")
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        else:
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    else:
        messages.error(request, "You cannot bid on this listing.")
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required  
def comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        content = request.POST["comment"]
        user = request.user
        comment = Comment(content=content, user=user, listing_id=listing_id)
        comment.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    
@login_required
def watch(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        user = request.user
        listing.watched_by.add(user)
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    
@login_required
def unwatch(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        user = request.user
        listing.watched_by.remove(user)
        return HttpResponseRedirect(reverse("watchlist"))
    
@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "listings": Listing.objects.filter(watched_by=request.user),
    })
        
        