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
    """
    Returns a render to the listing page
    """
    return render(request, 'auctions/listing.html', {
        'listing': Listing.objects.get(id=id)
    })

def watchlist(request):
    """
    Returns a render of the Watchlist page based on the request user
    """
    user = request.user

    if user.is_authenticated:
        return render(request, 'auctions/watchlist.html', {
            'watchlist': user.watchlist.all()
        })
    else:
        return HttpResponseRedirect(reverse('login'))

def addToWatchlist(request, listing):
    """
    Adds a listing to the request's user's watchlist
    """
    listing_object = Listing.objects.get(pk=listing)
    request.user.watchlist.add(listing_object)
    return HttpResponseRedirect(reverse('listing_page', kwargs={'id': listing}))

def removeFromWatchlist(request, listing):
    """
    Removes listing from user's watchlist
    """
    listing_object = Listing.objects.get(pk=listing)
    request.user.watchlist.remove(listing_object)
    return HttpResponseRedirect(reverse('listing_page', kwargs={'id': listing}))

def categories(request):
    """
    Returns a render of the categories page
    """
    return render(request, 'auctions/categories.html', {
        'categories': Listing.objects.values_list('category', flat=True)
    })

def categoryPage(request, category):
    """
    Returns a render of the individual category page, that contains all the listings that belong to said category
    """
    return render(request, 'auctions/category.html', {
        'listings': Listing.objects.filter(category__iexact=category),
        'category': category
    })

def makeBid(request, id):
    """
    Verifies if the bid value is greater than the listing's top bid value, if said condition is met, creates a bid with said value and sets the listing's top bid to be this created bid
    """
    value = int(request.POST['bid'])
    listing = Listing.objects.get(pk=id)

    if value > listing.top_bid.value:
        bidder = request.user
        bid = Bid(bidder=bidder, value=value)
        bid.save()
        listing.top_bid = bid
        listing.save()
        return HttpResponseRedirect(reverse('listing_page', kwargs={'id': id}))  
    else:
        return HttpResponse('Bid must be higher than current top bid')

def closeListing(request, id):
    """
    Closes listing
    """
    listing = Listing.objects.get(pk=id)
    listing.is_active = False
    listing.save()
    return HttpResponseRedirect(reverse('listing_page', kwargs={'id': id}))

def addComment(request, id):
    """
    Makes sure that the request method is POST, and creates a comment with the passed content from the template
    """
    if request.method == 'POST':
        author = request.user
        content = request.POST['comment']
        comment = Comment(author=author, content=content)
        comment.save()
        listing = Listing.objects.get(pk=id)
        listing.comments.add(comment)
        listing.save()
        return HttpResponseRedirect(reverse('listing_page', kwargs={'id': id}))
    else:
        return HttpResponseRedirect(reverse('listing_page', kwargs={'id': id}))