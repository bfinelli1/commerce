from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from  decimal import Decimal
from django.db.models import Max

from .models import User, auction_listings, comments, bids, watchlists


def index(request):
    return render(request, "auctions/index.html", {
        "listings": auction_listings.objects.all()
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
    mylisting = auction_listings.objects.get(id=listing_id)
    mycomments = comments.objects.filter(listing__id=listing_id)
    bid = bids.objects.filter(listing__id=listing_id)
    max = bids.objects.filter(listing__id=listing_id).aggregate(Max('bid'))
    max = max['bid__max']
    mycount = bids.objects.filter(listing__id=listing_id).count()
    return render(request, "auctions/listing.html", {
        "listing" : mylisting,
        "comments" : mycomments,
        "category" : mylisting.category,
        "bids" : bid,
        "maxbid" : max,
        "count" : mycount

    })

def newlisting(request):
    if request.method == "POST":
        t = request.POST["title"]
        desc = request.POST["description"]
        b = request.POST["bid"]
        url = request.POST["url"]
        cat = request.POST["category"]
        mynewlisting= auction_listings(title=t, description=desc, price=b, img_url=url, category=cat)
        mynewlisting.save()
    return render(request, "auctions/newlisting.html")

def comment(request, listing_id):
    if request.method == "POST":
        mycomment=request.POST["content"]
        currentuser=request.user
        newcomment = comments(comment=mycomment, user=currentuser, listing=auction_listings.objects.get(pk=listing_id))
        newcomment.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def watchlist(request):
    currentuser=request.user
    mywatchlist = watchlists.objects.filter(user=currentuser)
    return render(request, "auctions/watchlist.html", {
        "user" : currentuser,
        "watchlist" : mywatchlist

    })

def addtowatchlist(request, listing_id):
    if request.method =="POST":
        currentuser=request.user
        listing = auction_listings.objects.get(id=listing_id)
        #bids.objects.filter(listing__id=listing_id).count()
        newwatch = watchlists(user=currentuser, listing=listing)
        if watchlists.objects.filter(listing__id=listing_id, user=currentuser).count() >0:
            pass    
        else:
            newwatch.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def removefromwatchlist(request, listing_id):
    if request.method == "POST":
        currentuser=request.user
        listing = auction_listings.objects.get(id=listing_id)
        try:
            watch = watchlists.objects.get(user=currentuser, listing=listing)
        except watchlists.DoesNotExist:
            watch = None
        if watch:
            watch.delete()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    
def categories(request):
    pass

def bid(request, listing_id):
    if request.method == "POST":
        currentuser=request.user
        amount=request.POST["bid"]
        listing = auction_listings.objects.get(id=listing_id)
        max = bids.objects.filter(listing__id=listing_id).aggregate(Max('bid'))
        max = max['bid__max']
        price = listing.price
        if not max:
            max = price
        if Decimal(amount) > Decimal(price) and Decimal(amount) > max:
                newbid = bids(bid=Decimal(amount),user=currentuser, listing=listing)
                listing.price = Decimal(amount)
                listing.save()
                newbid.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))