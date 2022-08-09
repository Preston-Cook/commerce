from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from . import utils
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment

def index(request):
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.filter(is_active=True)
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

@login_required(login_url="/login")
def add(request):
    if request.method == "POST":
        title = request.POST["title"].strip()
        category = request.POST["category"]
        starting_bid = request.POST["starting_bid"]
        description = request.POST["description"].strip()
        image_url = request.POST["image_url"]
        seller_id = request.user.id

        bid = Bid(current_bid=starting_bid)
        bid.save()

        listing = Listing(title=title, category=category, description=description, image_url=image_url, seller_id=seller_id, price=bid)
        listing.save()

        if listing not in request.user.watchlist.all():
            request.user.watchlist.add(listing)

        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

    return render(request, "auctions/add.html")

@login_required(login_url="/login")
def listing(request, listing_id):
    
    listing = Listing.objects.get(pk=int(listing_id))
    comments = Comment.objects.filter(listing_id=listing_id)

    bid = listing.price

    return render(request, "auctions/listing.html", {
        "listing" : listing,
        "num_bids": bid.num_bids,
        "current_bid": bid.current_bid,
        "comments": comments,
        "watching": request.user in listing.watchers.all(),
        "highest_bidder": request.user.id == bid.highest_bidder_id,
        "is_seller" : request.user == listing.seller
    })

def watch(request):
    listing_id = request.POST["listing_id"]
    listing = Listing.objects.get(pk=int(listing_id))

    if request.POST.get('remove'):
        request.user.watchlist.remove(listing)
    else:
        request.user.watchlist.add(listing)
    
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def comment(request):
    text = request.POST['text']
    user = request.user
    listing_id = request.POST["listing_id"]
    listing = Listing.objects.get(pk=int(listing_id))
    comment = Comment(text=text, user=user, listing=listing)
    comment.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required(login_url="/login")
def account(request):
    watchlist = request.user.watchlist.all()
    active_listings = Listing.objects.filter(seller=request.user, is_active=True)
    closed_listings = Listing.objects.filter(seller=request.user, is_active=False)

    return render(request, "auctions/account.html", {
        "date": request.user.date_joined.strftime("%B %w, %Y"),
        "watchlist": watchlist,
        "active_listings": active_listings,
        "closed_listings": closed_listings
    })

@login_required(login_url="/login")
def bid(request):
    new_bid = float(request.POST['bid'])
    listing_id = request.POST["listing_id"]

    listing = Listing.objects.get(pk=int(listing_id))

    bid = listing.price
    current_bid = float(bid.current_bid)

    if listing not in request.user.watchlist.all():
            request.user.watchlist.add(listing)
    
    if new_bid < current_bid:
        comments = Comment.objects.filter(listing_id=listing_id)
        return render(request, "auctions/listing.html",{
            "listing" : listing,
            "bids" : bid.num_bids,
            "current_bid" : bid.current_bid,
            "comments" : comments,
            "watching": request.user in listing.watchers.all(),
            "highest_bidder": request.user.id == bid.highest_bidder_id,
            "message" : "Bid must be greater than current bid",
            "is_seller" : request.user == listing.seller
        })

    bid.highest_bidder_id = request.user.id
    bid.current_bid = new_bid
    bid.num_bids += 1
    bid.save()

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required(login_url="/login")
def close(request):
    listing_id = request.POST["listing_id"]
    listing = Listing.objects.get(pk=int(listing_id))

    listing.is_active = False
    listing.save()

    bid = listing.price
    comments = Comment.objects.filter(listing_id=listing_id)

    return render(request, "auctions/listing.html",{
            "listing" : listing,
            "bids" : bid.num_bids,
            "current_bid" : bid.current_bid,
            "comments" : comments,
            "watching": request.user in listing.watchers.all(),
            "highest_bidder": request.user.id == bid.highest_bidder_id,
            "is_seller" : request.user == listing.seller
        })

@login_required(login_url="/login")
def search(request):
    query = request.GET["q"].lower()
    categories = list(map(str.lower, utils.categories))
    query_specifier = [category.title() for category in categories if query in category.split() or query == category]
    
    if query_specifier:
        results = Listing.objects.filter(category=query_specifier[0])
    else:
        results = Listing.objects.filter(is_active=True, title__icontains=query)
    
    return render(request, "auctions/search.html", {
        "query" : query,
        "results" : results
    })

    