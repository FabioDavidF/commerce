from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.all()
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


def createListing(request):
    """
    returns a render of the create page if the request method is GET
    If the request method is POST, the function gets the data from html form and saves it as a listing
    """
      
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'auctions/create_listing.html')

        elif request.method =='POST':
            creator = request.user
            title = request.POST['title']
            description = request.POST['description']

            if request.POST['starting_bid'] == '':
                starting_bid = 0
            else:
                starting_bid = request.POST['starting_bid']
            
            top_bid = Bid(bidder=request.user, value=starting_bid)
            top_bid.save()
            
            if request.POST['img_url']:
                img_url = request.POST['img_url']
            else:
                img_url = None

            if request.POST['category']:
                category = request.POST['category']
            else:
                category = None

            listing = Listing(creator=creator,
            title=title,
            description=description,
            bid_quantity=0,
            starting_bid=starting_bid,
            top_bid = top_bid,
            img_url=img_url,
            category=category)
            listing.save()

            return HttpResponseRedirect(reverse('listing_page', kwargs={'id': listing.id}))
    else:
        return HttpResponseRedirect(reverse('login'))

def listing(request, id):
    return render(request, 'auctions/listing.html', {
        'listing': Listing.objects.get(id=id)
    })

def watchlist(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'auctions/watchlist.html', {
            'watchlist': user.watchlist.all()
        })
    else:
        return HttpResponseRedirect(reverse('login'))

def addToWatchlist(request, listing):
    listing_object = Listing.objects.get(pk=listing)
    request.user.watchlist.add(listing_object)
    return HttpResponseRedirect(reverse('listing_page', kwargs={'id': listing}))

def removeFromWatchlist(request, listing):
    listing_object = Listing.objects.get(pk=listing)
    request.user.watchlist.remove(listing_object)
    return HttpResponseRedirect(reverse('listing_page', kwargs={'id': listing}))

def categories(request):
    return render(request, 'auctions/categories.html', {
        'categories': Listing.objects.values_list('category', flat=True)
    })

def categoryPage(request, category):
    return render(request, 'auctions/category.html', {
        'listings': Listing.objects.filter(category__iexact=category),
        'category': category
    })

def makeBid(request, id):
    value = int(request.POST['bid'])
    listing = Listing.objects.get(pk=id)
    if value > listing.top_bid:
        bidder = request.user
        bid = Bid(bidder=bidder, value=value)
        if bid.value > listing.top_bid:
            listing.top_bid = bid.value
            listing.save()
            bid.save()
            return HttpResponseRedirect(reverse('listing_page', kwargs={'id': id}))
        else:
            return HttpResponse('Bid must be higher than current top bid')
    else:
        return HttpResponseRedirect(reverse('listing_page', kwargs={'id': id}))
